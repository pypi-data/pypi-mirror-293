"""Provides classes and methods for mapping from OnePlan type defs to OpenAPI 3.1 schema types."""

from collections.abc import Iterator
from typing import Any, Optional, Self

from yaml import dump as yaml_dump

from oneplan_sdk.sync.consts import MARKER_TYPE_COLLECTION, MARKER_TYPE_DICTIONARY
from oneplan_sdk.sync.interfaces import get_array_atomic_type, get_dict_atomic_types
from oneplan_sdk.sync.schema import Schema
from oneplan_sdk.sync.util import get_sanitized_schema_type


class OpenApiTypeMapping:
    """Provides a mapping of OnePlan custom type definitions to Open API 3.1 schema types."""

    __instance = None

    def __new__(cls):
        """Creates or returns an instance of the mapping."""
        if cls.__instance is None:
            cls.__instance = super(OpenApiTypeMapping, cls).__new__(cls)
            cls.__instance._initialize()
        return cls.__instance

    def _initialize(self):
        """Creates the empty mapping dictionary."""
        self.mapping: dict[str, Schema] = {}

    def register_type(self, custom_type: str, schema: Schema) -> None:
        """Adds the schema for a custom type to the mapping."""
        self.mapping[get_sanitized_schema_type(custom_type)] = schema

    def load(self, typecasts: dict[str, Schema]) -> Self:
        """Populates the mapping from known OnePlan custom types to OpenAPI 3.1 types.

        Note: Since CustomTypeMapping is a singleton,
        we only need to populate it once without returning anything.
        """
        mapping = OpenApiTypeMapping()

        for custom_type, schema in typecasts.items():
            mapping.register_type(custom_type, schema)

        return self

    def get_schema(self, custom_type: str) -> Optional[Schema]:
        """Returns the schema that corresponds to the custom type."""
        if custom_type.startswith(MARKER_TYPE_COLLECTION):
            return self.get_schema_as_array(custom_type)
        if custom_type.startswith(MARKER_TYPE_DICTIONARY):
            return self.get_schema_as_dict(custom_type)
        return self.mapping.get(get_sanitized_schema_type(custom_type))

    def get_schema_as_array(self, custom_type: str) -> Optional[Schema]:
        """Returns a schema that is an array of items matching the custom type."""
        atomic_type = get_array_atomic_type(custom_type)
        schema = self.get_schema(atomic_type)

        if schema:
            return Schema(
                name=get_sanitized_schema_type(custom_type),
                type="array",
                items=schema,
                description=f"An array of {atomic_type}s",
            )

    def get_schema_as_dict(self, custom_type: str) -> Optional[Schema]:
        """Returns a schema that is an array of items matching the custom type."""
        key, value = get_dict_atomic_types(custom_type)
        key_schema = self.get_schema(key)
        value_schema = self.get_schema(value)

        if key_schema and value_schema:
            return Schema(
                name=get_sanitized_schema_type(custom_type),
                type="object",
                additionalProperties=value_schema,
                description=f"A dictionary with {key} keys and {key} values.",
                example={key_schema.example: value_schema.example},
            )

    def has_schema(self, custom_type: str) -> bool:
        """Returns True if the mapping has a schema for the custom type."""
        return self.get_schema(custom_type) is not None

    def to_dict(self) -> dict[str, Any]:
        """Returns a dictionary representation of the mapping."""
        return {k: v.to_dict() for k, v in self.mapping.items()}

    def to_yaml(self) -> str:
        """Returns a yaml representation of the mapping."""
        return yaml_dump(self.to_dict(), sort_keys=False)

    def __iter__(self) -> Iterator[str]:
        """Returns an iterator with the custom type keys in the mapping.

        The iterator yields safe copy of the keys in the mapping,
        generated as of the time when this method was invoked.
        """
        return iter(tuple(self.mapping))

    def __len__(self) -> int:
        """Returns the number of the keys in the mapping."""
        return len(self.mapping)

    def __contains__(self, custom_type) -> bool:
        """Returns True if the custom type is found in the mapping.

        This lookup supports collection and dictionary types in the OpenPlan API.
        """
        return self.get_schema(custom_type) is not None


TYPE_CASTS: dict[str, Schema] = {
    "globally unique identifier": Schema(
        name="globally_unique_identifier",
        type="string",
        format="uuid",
        description="A UUID4 identifier",
        example="123e4567-e89b-12d3-a456-426614174000",
    ),
    "string": Schema(
        name="string", type="string", description="Any string", example="Big jet plane."
    ),
    "date": Schema(
        name="date",
        type="string",
        format="date-time",
        description="A datetime stamp",
        example="2024-07-16T11:30:05.7799278+00:00",
    ),
    "time interval": Schema(
        name="time_interval",
        type="string",
        pattern=r"^([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\.[0-9]{7}$",
    ),
    "integer": Schema(
        name="integer", type="integer", description="An integer", example=[-42, 42]
    ),
    "unsigned integer": Schema(
        name="unsigned_integer",
        type="integer",
        minimum=0,
        description="A positive integer",
        example=42,
    ),
    "decimal number": Schema(
        name="decimal_number",
        type="number",
        format="double",
        minimum=0,
        description="A positive decimal number",
        example=42.0,
    ),
    "boolean": Schema(
        name="boolean",
        type="boolean",
        description="A boolean value",
        example=["true", "false"],
    ),
    "URI": Schema(name="URI", type="string", format="uri"),
    "Object": Schema(name="Object", type="object"),
}

__all__ = ["OpenApiTypeMapping", "TYPE_CASTS"]
