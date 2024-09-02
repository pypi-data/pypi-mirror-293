"""Provides a model for an OpenAPI 3.1 type schema."""

from dataclasses import dataclass, fields
from typing import Any, Literal, Optional, Self, Union

from yaml import dump as yaml_dump

from oneplan_sdk.sync.consts import SCHEMA_REF_PREFIX

TNativeOpenApiType = Literal[
    "string", "integer", "number", "boolean", "object", "array"
]
TNativeOpenApiFormat = Literal[
    "uuid", "password", "date-time", "int32", "int64", "float", "double"
]


@dataclass
class Schema:
    """Encapsulates OpenAPI 3.1 schema type attributes.

    The extra `name` attribute is used internally
    for the generation of $ref component references
    upon generation of the OpenAPI specification doc.
    """

    name: str
    type: TNativeOpenApiType
    format: Optional[TNativeOpenApiFormat] = None
    pattern: Optional[str] = None
    description: Optional[str] = None
    example: Any = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    enum: Optional[list[Any]] = None
    properties: Optional[dict[str, Self]] = None
    required: Optional[list[str]] = None
    items: Optional[Self] = None  # For array types
    additionalProperties: Optional[Union[dict, Self]] = (
        None  # For dictionaries with arbitrary properties
    )

    @property
    def is_array(self) -> bool:
        """Returns True if the type is an array."""
        return self.type == "array"

    @property
    def is_dict(self) -> bool:
        """Returns True if the type is a dictionary."""
        return self.type == "object" and self.additionalProperties is not None

    @property
    def ref(self) -> str:
        """Returns the fully qualified $ref to the schema in the OpenApi 3.0 doc."""
        if self.is_dict:
            suffix = self.additionalProperties.name
        elif self.is_array:
            suffix = self.items.name
        else:
            suffix = self.name

        return f"{SCHEMA_REF_PREFIX}{suffix}"

    def to_ref(self) -> dict[str, str]:
        """Returns a $ref representation of the schema."""
        return {"$ref": self.ref}

    def to_dict(self) -> dict[str, str | dict]:
        """Returns a dictionary representation of the schema."""

        def _to_dict(obj):
            if isinstance(obj, Schema):
                if obj.is_array and obj.items:
                    return {"type": "array", "items": obj.items.to_ref()}
                if obj.is_dict:
                    return {
                        "type": "object",
                        "additionalProperties": obj.additionalProperties.to_ref(),
                    }
                return obj.to_ref()
            elif isinstance(obj, dict):
                return _to_sanitized_dict(obj)
            elif isinstance(obj, list):
                return [_to_dict(v) for v in obj]
            else:
                return obj

        def _to_sanitized_dict(mapping):
            return {
                k: _to_dict(v)
                for k, v in mapping.items()
                if v is not None and k != "name"
            }

        attrs = {f.name for f in fields(self) if f.name != "name"}
        return {
            attr: _to_dict(getattr(self, attr))
            for attr in attrs
            if getattr(self, attr) is not None
        }

    def to_yaml(self) -> str:
        """Returns a yaml representation of the schema."""
        return yaml_dump(self.to_dict(), sort_keys=False)


__all__ = ["Schema"]
