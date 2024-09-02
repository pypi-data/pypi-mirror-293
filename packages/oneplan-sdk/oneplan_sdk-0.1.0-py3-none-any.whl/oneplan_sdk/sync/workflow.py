"""Implements the OnePlan API synchronization and OpenAPI doc generation workflow."""

from dataclasses import asdict

from bs4 import BeautifulSoup
from yaml import dump as yaml_dump

from oneplan_sdk.sync.client import (
    add_client_artefacts_to_package,
    generate_python_client,
    sanitize_client_files,
)
from oneplan_sdk.sync.consts import (
    MARKER_ENUMERATION,
    PATH_ARTEFACTS,
    PATH_ARTEFACTS_SPEC,
)
from oneplan_sdk.sync.docs import (
    list_local_models,
    read_local_doc,
    sync_docs,
    sync_models,
)
from oneplan_sdk.sync.interfaces import IApiEnumeration, IApiModel
from oneplan_sdk.sync.mapping import TYPE_CASTS, OpenApiTypeMapping, Schema
from oneplan_sdk.sync.parsers import parse_enumeration_table, parse_model_table
from oneplan_sdk.sync.spec import (
    OpenApiSpec,
    add_endpoints_to_spec,
    add_schemas_to_spec,
    add_security_scheme_to_spec,
    add_tags_to_spec,
    generate_spec_base,
    get_tags_for_spec,
)
from oneplan_sdk.sync.util import ensure_artefacts_path

TModels = dict[str, IApiModel]
TEnumerations = dict[str, IApiEnumeration]


def load_models_and_enumerations() -> tuple[TModels, TEnumerations]:
    """Returns a tuple of dicts with OnePlan API custom models and enumerations."""
    models: dict[str, IApiModel] = {}
    enumerations: dict[str, IApiEnumeration] = {}

    for meta in list_local_models():
        doc = read_local_doc(meta.local_path)
        soup = BeautifulSoup(doc, "html.parser")
        table = soup.find("table")

        if (
            not table
        ):  # see e.g. https://eu.oneplan.ai/ApiHelp/ResourceModel?modelName=IntPtr
            continue

        if MARKER_ENUMERATION in doc:
            enumeration = parse_enumeration_table(soup.find("table"), meta)
            enumerations[enumeration.name] = enumeration
        else:
            model = parse_model_table(soup.find("table"), meta)
            models[model.name] = model

    return models, enumerations


def register_enumeration(
    mapping: OpenApiTypeMapping, enumeration: IApiEnumeration
) -> None:
    """Adds a OnePlan API enumeration as a enum schema in the OpenAPI mapping."""
    mapping.register_type(
        enumeration.name,
        Schema(
            name=enumeration.name,
            type="string",
            enum=sorted([field.name for field in enumeration.fields]),
        ),
    )


def register_custom_model(
    model: IApiModel,
    mapping: OpenApiTypeMapping,
    models: dict[str, IApiModel] | None = None,
) -> None:
    """Registers a custom OnePlan API model as a object schema in the OpenAPI mapping.

    Note: This method is one-step recursive.
    In combination with a higher-level while-loop
    (see `oneplan_sdk.sync.workflow.register_custom_models`),
    this deal with tricky cases in the model graph, where:
    a) a model may refer to itself, or
    b) there is a cyclical loop in the model graph involving two or more models.
    """
    if models:
        for field in model.fields:
            if not field.has_nested_model:
                continue

            atomic_types = field.atomic_type if field.is_dict else [field.atomic_type]
            for atomic_type in atomic_types:
                if (
                    atomic_type != model.name
                    and atomic_type in models
                    and not mapping.has_schema(atomic_type)
                ):
                    register_custom_model(models[atomic_type], mapping)

    mapping.register_type(
        model.name,
        Schema(
            name=model.name,
            type="object",
            properties={
                field.name: mapping.get_schema(field.type) for field in model.fields
            },
        ),
    )


def register_custom_models(mapping: OpenApiTypeMapping, models: TModels) -> None:
    """Registers all OnePlan API models as object schemas in the OpenAPI mapping.

    For implementation details, see the notes to
    `oneplan_sdk.sync.workflow.register_custom_model`.
    """
    last_len = 0

    while True:
        pending_models = [
            model for model in models.values() if not mapping.has_schema(model.name)
        ]

        if len(pending_models) in (0, last_len):
            break

        last_len = len(pending_models)

        for model in pending_models:
            register_custom_model(model, mapping, models)


def load_mapping() -> None:
    """Registers all OnePlan API types (native, enums and objects) in the OnePlan API mapping."""
    mapping = OpenApiTypeMapping().load(TYPE_CASTS)
    models, enumerations = load_models_and_enumerations()

    for enumeration in enumerations.values():
        register_enumeration(mapping, enumeration)

    register_custom_models(mapping, models)


def generate_open_api_spec() -> OpenApiSpec:
    """Autogenerates the OpenAPI spec based on the OnePlan API docs."""
    ensure_artefacts_path()
    mapping = OpenApiTypeMapping()

    with open(PATH_ARTEFACTS / "schemas.yaml", "wt") as f:
        f.write(mapping.to_yaml())

    spec = generate_spec_base(version="1.0.0")
    tags, endpoint_tags = get_tags_for_spec()

    add_schemas_to_spec(spec, mapping)
    add_security_scheme_to_spec(spec)
    add_tags_to_spec(spec, tags)
    add_endpoints_to_spec(spec, mapping, endpoint_tags)

    with open(PATH_ARTEFACTS_SPEC, "wt") as f:
        f.write(yaml_dump(asdict(spec), sort_keys=False))

    return spec


def generate_client(spec: OpenApiSpec, force_regen: bool = False) -> None:
    """Generates and processes the API python client."""
    generate_python_client(spec, force_regen=force_regen)
    add_client_artefacts_to_package()
    sanitize_client_files()


def generate_sdk(force_client_regen: bool = False) -> None:
    """Synchronizes the OnePlan API docs with the local cache."""
    sync_docs()
    sync_models()
    load_mapping()
    spec = generate_open_api_spec()
    generate_client(spec, force_regen=force_client_regen)


__all__ = ["generate_sdk"]
