"""Provides an interface for document metadata."""

from html import unescape
from pathlib import Path
from textwrap import dedent
from typing import Literal, NamedTuple, Self

from oneplan_sdk.sync.consts import (
    MARKER_TYPE_COLLECTION,
    MARKER_TYPE_DICTIONARY,
    ONEPLAN_API_URL_BASE,
    ONEPLAN_API_URL_HELP_BASE,
    PATH_CACHE,
    RE_API_GROUP,
)
from oneplan_sdk.sync.util import get_array_atomic_type, get_dict_atomic_types

TRequestMethod = Literal["GET", "POST", "PATCH", "PUT", "DELETE"]


class IDocMeta(NamedTuple):
    """Provides a model for doc page attributes."""

    url_path: str
    method: TRequestMethod
    endpoint: str

    @property
    def url(self) -> str:
        """Returns the fully qualified url for the doc page."""
        return f"{ONEPLAN_API_URL_HELP_BASE}/Api/{self.url_path}"

    @property
    def local_path(self) -> Path:
        """Returns the path to the locally hashed version of the doc."""
        return PATH_CACHE / f"{self.url_path}.html"

    @property
    def sanitized_endpoint(self) -> str:
        """Returns an unescaped endpoint string."""
        return unescape(self.endpoint)

    @property
    def path(self) -> str:
        """Returns the relative path portion of an endpoint."""
        return self.sanitized_endpoint.lstrip("api").split("?")[0]

    @property
    def openapi_method(self) -> str:
        """Returns the OpenApi spec compliant (lower-cased) method name."""
        return self.method.lower()

    @property
    def endpoint_group(self) -> str:
        """Returns the logical group the API point belongs to."""
        return RE_API_GROUP.match(self.sanitized_endpoint).group(1)

    def __str__(self) -> str:
        """Returns a str representation of the named tuple."""
        string = f"""
        {self.__class__.__name__}(
            url_path: {self.url_path},
            method: {self.method},
            endpoint: {self.endpoint},
            __accessors__: {{
                local_path: {self.local_path.name},
                endpoint_group: {self.endpoint_group}
            }}
        )
        """

        return dedent(string)


class IApiModelMeta(NamedTuple):
    """Provides a model for API model page attributes."""

    url_path: str

    @property
    def model_name(self) -> str:
        """Returns the name of the API data model."""
        return self.url_path.split("=")[1]

    @property
    def url(self) -> str:
        """Returns the fully qualified url for the doc page."""
        return f"{ONEPLAN_API_URL_BASE}{self.url_path}"

    @property
    def local_path(self) -> Path:
        """Returns the path to the locally hashed version of the doc."""
        return PATH_CACHE / f"MODEL-{self.model_name}.html"

    @classmethod
    def from_local_path(cls, path: Path) -> Self:
        """Returns an instance of the model meta based on local path info."""
        model_name = path.stem.replace("MODEL-", "")
        url_path = f"ApiHelp/ResourceModel?modelName={model_name}"
        return cls(url_path=url_path)

    def __str__(self) -> str:
        """Returns a str representation of the named tuple."""
        string = f"""
        {self.__class__.__name__}(
            url_path: {self.url_path},
            __accessors__: {{
                model_name: {self.model_name},
                local_path: {self.local_path.name}
            }}
        )
        """

        return dedent(string)


class IApiModelField(NamedTuple):
    """Provides a model for an OpenPlan API model field."""

    name: str
    description: str
    type: str
    additional_information: str | None = None

    @property
    def is_array(self) -> bool:
        """Returns True if the type is an array."""
        return self.type.startswith(MARKER_TYPE_COLLECTION)

    @property
    def is_dict(self) -> bool:
        """Returns True if the type is a dictionary."""
        return self.type.startswith(MARKER_TYPE_DICTIONARY)

    @property
    def atomic_type(self) -> str | tuple[str, str]:
        """Returns the atomic type for the field.

        This would be a key-value type pair in the case of a dictionary type.
        """
        if self.is_array:
            return get_array_atomic_type(self.type)
        if self.is_dict:
            return get_dict_atomic_types(self.type)
        return self.type

    @property
    def has_nested_model(self) -> bool:
        """Returns True if the type refers to another model."""
        atomic_types = self.atomic_type if self.is_dict else self.atomic_type

        for atomic_type in atomic_types:
            if atomic_type[0].upper() == atomic_type[0] and atomic_type != "Object":
                return True

        return False

    @property
    def nested_model_meta(self) -> IApiModelMeta | None:
        """Returns the url for the nested model, if it exists."""
        if not self.has_nested_model:
            return

        beg = self.type.index("<a href=")
        end = self.type.index("</a>") + len("<a/>")
        url_path = self.type[beg:end]
        return IApiModelMeta(url_path)

    def __str__(self) -> str:
        """Returns a str representation of the named tuple."""
        string = f"""
        {self.__class__.__name__}(
            name: {self.name},
            type: {self.type},
            __accessors__: {{
                is_array: {self.is_array},
                has_nested_model: {self.has_nested_model}
            }}
        )
        """

        return dedent(string)


class IApiEnumerationMember(NamedTuple):
    """Provides a model for an OpenPlan API enumeration member."""

    name: str
    value: str
    description: str

    @property
    def native_value(self) -> int | str:
        """Returns the native type value of the enumeration member."""
        if self.value.lstrip("-").isnumeric():
            return int(self.value)
        return self.value


class IApiObject(NamedTuple):
    """Provides a base model for a OpenPlan API models and enumerations."""

    name: str | None
    fields: tuple[IApiModelField | IApiEnumerationMember, ...]

    def __str__(self) -> str:
        """Returns a str representation of the named tuple."""
        fields = ""
        for field in self.fields:
            fields += f""",{field}"""

        string = f"""
        {self.__class__.__name__}(
            name: {self.name},
            fields: (
                {fields}
            )
        )
        """

        return dedent(string)


class IApiModel(IApiObject):
    """Provides a model for a OpenPlan API model field."""

    fields: tuple[IApiModelField, ...]

    @property
    def has_nested_models(self) -> bool:
        """Returns True if the model has nested models."""
        return any(field.has_nested_model for field in self.fields)


class IApiEnumeration(IApiObject):
    """Provides a model for a OnePlan API enumeration."""

    fields: tuple[IApiEnumerationMember, ...]


__all__ = [
    "TRequestMethod",
    "IDocMeta",
    "IApiModelMeta",
    "IApiModel",
    "IApiModelField",
    "IApiEnumeration",
    "IApiEnumerationMember",
]
