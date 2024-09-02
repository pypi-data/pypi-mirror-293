"""Provides functionality for compiling the output OpenApi spec document for the OnePlan API."""

from dataclasses import dataclass, field, fields
from typing import Any

from bs4 import BeautifulSoup

from oneplan_sdk.sync.consts import (
    MARKER_DEFAULT_VALUE,
    ONEPLAN_API_URL_BASE,
    ONEPLAN_API_URL_HELP_BASE,
    PATH_ONEPLAN_API_DOCS,
    RE_SPACES,
    RE_URL_PARAMS,
    SECURITY_SCHEME_NAME,
)
from oneplan_sdk.sync.docs import list_docs_info, read_local_doc
from oneplan_sdk.sync.interfaces import IApiModelField, IDocMeta
from oneplan_sdk.sync.mapping import OpenApiTypeMapping, Schema
from oneplan_sdk.sync.parsers import parse_model_table

TEndpointTags = dict[tuple[str, str], str]


@dataclass
class OpenApiSpecInfo:
    """Provides a data model for an OpenApi 3.0 spec info."""

    title: str
    description: str
    version: str


@dataclass
class OpenApiSpecExternalDocs:
    """Provides a data model for an OpenApi 3.0 external docs."""

    description: str
    url: str


@dataclass
class OpenApiSpecServer:
    """Provides a data model for an OpenApi 3.0 server."""

    url: str


@dataclass
class OpenApiSpecTag:
    """Provides a data model for an OpenApi 3.0 tag."""

    name: str


@dataclass
class OpenApiSpecComponents:
    """Provides a data model for an OpenApi 3.0 tag."""

    schemas: dict[str, Any] = field(default_factory=dict)
    securitySchemes: dict[str, Any] = field(default_factory=dict)


@dataclass
class OpenApiMethodSpec:
    """Provides a data model for an OpenApi 3.0 path method spec."""

    tags: list[OpenApiSpecTag] = field(default_factory=list)
    parameters: dict[str, Any] | None = field(default=None)
    requestBody: dict[str, Any] | None = field(default=None)
    responses: dict[str, Any] | None = field(default=None)
    security: list[dict[str, Any]] | None = field(default=None)

    def to_dict(self) -> dict[str, Any]:
        """Returns a dict representation of the method spec."""
        return {
            f.name: getattr(self, f.name)
            for f in fields(self)
            if getattr(self, f.name) is not None
        }


@dataclass
class OpenApiSpec:
    """Provides a data model for an OpenApi 3.0 spec."""

    openapi: str
    info: OpenApiSpecInfo
    externalDocs: OpenApiSpecExternalDocs
    servers: list[OpenApiSpecServer]
    tags: list[OpenApiSpecTag] = field(default_factory=list)
    paths: dict[str, OpenApiMethodSpec] = field(default_factory=dict)
    components: OpenApiSpecComponents = field(default_factory=OpenApiSpecComponents)
    security: list[dict[str, Any]] = field(default_factory=list)


def generate_spec_base(version: str) -> OpenApiSpec:
    """Returns a base OpenApiSpec instance for further customisation."""
    return OpenApiSpec(
        openapi="3.0.3",
        info=OpenApiSpecInfo(
            title="OnePlan API",
            description=(
                "This is an automatically generated OpenAPI specification "
                "for the OnePlan API based on the api help docs."
            ),
            version=version,
        ),
        externalDocs=OpenApiSpecExternalDocs(
            description="The official OnePlan API help pages",
            url=ONEPLAN_API_URL_HELP_BASE,
        ),
        servers=[OpenApiSpecServer(url=f"{ONEPLAN_API_URL_BASE}/api")],
    )


def add_schemas_to_spec(spec: OpenApiSpec, mapping: OpenApiTypeMapping) -> None:
    """Adds custom component schemas to the OpenApi spec."""
    spec.components.schemas.update(mapping.to_dict())


def add_security_scheme_to_spec(spec: OpenApiSpec) -> None:
    """Adds the security scheme to the OnePlan OpenAPI spec."""
    spec.components.securitySchemes.update(
        {SECURITY_SCHEME_NAME: dict(type="http", scheme="basic")}
    )
    spec.security.append({SECURITY_SCHEME_NAME: []})


def get_tags_for_spec() -> tuple[list[OpenApiSpecTag], TEndpointTags]:
    """Returns a tuple with schema tags and a mapping of endpoints to tags."""
    soup = BeautifulSoup(read_local_doc(PATH_ONEPLAN_API_DOCS), "html.parser")
    tags: list[OpenApiSpecTag] = []
    endpoint_tags: TEndpointTags = {}

    for element in soup.findAll(["h2", "a"]):
        if element.name == "h2":
            if element.text == "Introduction":
                continue
            tags.append(OpenApiSpecTag(name=element.text))
            continue

        method, endpoint = element.text.split(" ")
        endpoint_tags[(method, endpoint)] = tags[-1].name

    return tags, endpoint_tags


def add_tags_to_spec(spec: OpenApiSpec, tags: list[OpenApiSpecTag]) -> None:
    """Adds logical endpoint grouping tags to the OpenApi spec."""
    spec.tags.extend(tags)


def add_payload_schema(
    schema_name: str, mapping: OpenApiTypeMapping, explicit: bool = False
) -> dict[str, Any]:
    """Returns a dict with payload schemas for supported content types in OnePlan API."""
    schema = mapping.get_schema(schema_name)
    return {
        "application/json": {
            "schema": schema.to_dict() if explicit or schema.is_array else schema.to_ref()
        }
    }


def get_field_default_value(model_field: IApiModelField) -> str | None:
    """Returns the default value for a field of None if it doesn't have any."""
    if not model_field.additional_information.startswith(MARKER_DEFAULT_VALUE):
        return
    
    return model_field.additional_information.replace(MARKER_DEFAULT_VALUE, "")


def get_uri_param_schemas(
    soup: BeautifulSoup, meta: IDocMeta, mapping: OpenApiTypeMapping
) -> dict[str, tuple[Schema, str | None]] | bool:
    """Returns the schemas for the path and query params in a URI (if any)."""
    header = soup.find("h3", string="URI Parameters")

    if not header:
        print("URI Parameters", meta.method, meta.sanitized_endpoint)
        return False

    table = header.find_next(["table", "h3"])

    if table is None or table.name != "table":
        return True

    path_param_model = parse_model_table(table)

    return {
        field.name: (
            mapping.get_schema(field.type),
            get_field_default_value(field)
        )
        for field in path_param_model.fields
    }


def get_request_schema_name(soup: BeautifulSoup) -> str | None:
    """Returns the name of the schema for the request payload."""
    header = soup.find("h3", string="Body Parameters")

    if not header:
        return

    anchor = header.find_next(["a", "h3"])
    if anchor is None or anchor.name != "a":
        return

    return anchor.text


def get_response_schema_name(
    soup: BeautifulSoup, meta: IDocMeta, mapping: OpenApiTypeMapping
) -> tuple[str, bool] | tuple[None, None]:
    """Returns the name of the schema for the response payload."""
    header = soup.find("h3", string="Resource Description")

    if not header:
        return None, None

    schema_name = RE_SPACES.sub(" ", (header.find_next("p").next_sibling.strip()))

    anchor = header.find_next("a")
    if anchor:
        schema_name = f"{schema_name} {anchor.text}".strip()
        return schema_name, False

    if not mapping.get_schema(schema_name):
        print("RESPONSE", meta.method, meta.sanitized_endpoint)
        print(schema_name, mapping.get_schema(schema_name))
        print("----")
        return None, None

    return schema_name, True


def add_path_param_schemas(
    spec: OpenApiMethodSpec, param_schemas: dict[str, tuple[Schema, str | None]], meta: IDocMeta
) -> None:
    """Adds path URI parameter schemas to an OpenApi method spec."""
    path_params = [
        name for name in param_schemas if name in RE_URL_PARAMS.findall(meta.path)
    ]

    try:
        parameters = []

        for param_name, (schema, default) in param_schemas.items():
            param = {
                "name": param_name,
                "in": "path" if param_name in path_params else "query",
                "required": default is None,
                "schema": schema.to_ref(),
            }
        
            if default:
                param["default"] = default
        
            parameters.append(param)
        
        spec.parameters = parameters
    except AttributeError:
        print("Schemas", meta.sanitized_endpoint)


def add_request_body_schema(
    spec: OpenApiMethodSpec, schema_name: str, mapping: OpenApiTypeMapping
) -> None:
    """Adds a request body schema to an OpenApi method spec."""
    spec.requestBody = {
        "content": add_payload_schema(schema_name, mapping),
        "required": True,
    }


def add_response_schemas(
    spec: OpenApiMethodSpec,
    schema_name: str,
    explicit: bool,
    mapping: OpenApiTypeMapping,
) -> None:
    """Adds the response schemas to an OpenApi method spec."""
    spec.responses = {
        "200": {
            "description": schema_name,
            "content": add_payload_schema(schema_name, mapping, explicit=explicit),
        }
    }


def add_endpoint_to_spec(
    meta: IDocMeta, spec: OpenApiSpec, mapping: OpenApiTypeMapping, tags: TEndpointTags
) -> None:
    """Adds the definition for a single endpoint/method pair to the OpenApi spec."""
    if not meta.local_path.exists():
        return
    soup = BeautifulSoup(read_local_doc(meta.local_path), "html.parser")

    tag = tags[(meta.method, meta.sanitized_endpoint)]

    uri_param_schemas = get_uri_param_schemas(soup, meta, mapping)
    request_schema_name = get_request_schema_name(soup)
    response_schema_name, explicit = get_response_schema_name(soup, meta, mapping)

    method_spec = OpenApiMethodSpec(tags=[tag], security=[{SECURITY_SCHEME_NAME: []}])

    # TODO: see DependencyType in POST-api-tasks-dependency-TaskId-DepId_Type_Lag_LagUnit
    # TODO: Verify required params
    if uri_param_schemas is False:
        return
    if type(uri_param_schemas) is dict:
        add_path_param_schemas(method_spec, uri_param_schemas, meta)

    if request_schema_name:
        add_request_body_schema(method_spec, request_schema_name, mapping)

    if response_schema_name:
        add_response_schemas(method_spec, response_schema_name, explicit, mapping)

    if meta.path not in spec.paths:
        spec.paths[meta.path] = {}

    spec.paths[meta.path][meta.openapi_method] = method_spec.to_dict()


def add_endpoints_to_spec(
    spec: OpenApiSpec, mapping: OpenApiTypeMapping, tags: TEndpointTags
) -> None:
    """Adds all endpoint paths to the OpenApi spec."""
    for meta in filter(lambda x: x.method != "", list_docs_info()):
        add_endpoint_to_spec(meta, spec, mapping, tags)


__all__ = [
    "generate_spec_base",
    "add_schemas_to_spec",
    "add_security_scheme_to_spec",
    "get_tags_for_spec",
    "add_endpoints_to_spec",
    "add_tags_to_spec",
    "add_endpoints_to_spec",
]
