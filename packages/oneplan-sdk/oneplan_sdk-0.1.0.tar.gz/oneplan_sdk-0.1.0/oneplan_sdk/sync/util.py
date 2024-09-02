"""Includes utility functions for the sync module of the onenplan_sdk package."""

from pathlib import Path

from oneplan_sdk.sync.consts import (
    MARKER_TYPE_COLLECTION,
    PATH_ARTEFACTS,
    PATH_CACHE,
    PATH_CLIENT,
    RE_DICTIONARY_TYPE_PARTS,
    RE_SPACES,
)


def ensure_path(path: Path) -> None:
    """Ensures the local cache path is ready."""
    path.mkdir(parents=True, exist_ok=True)


def ensure_cache_path() -> None:
    """Ensures the local cache path is ready."""
    ensure_path(PATH_CACHE)


def ensure_artefacts_path() -> None:
    """Ensures the local cache path is ready."""
    ensure_path(PATH_ARTEFACTS)


def ensure_client_path() -> None:
    """Ensures the local cache path is ready."""
    ensure_path(PATH_CLIENT)


def get_array_atomic_type(field_type: str) -> str:
    """Returns the atomic type for an array type."""
    return field_type.replace(MARKER_TYPE_COLLECTION, "").strip()


def get_dict_atomic_types(field_type: str) -> tuple[str, str]:
    """Returns the atomic type for an dict type."""
    return RE_DICTIONARY_TYPE_PARTS.match(RE_SPACES.sub(" ", field_type)).groups()


def get_sanitized_schema_type(schema_type: str) -> str:
    """Returns the sanitized name of a schema type, compliant with OpenAPI specs."""
    return RE_SPACES.sub(" ", schema_type).replace(" ", "_")


__all__ = [
    "ensure_cache_path",
    "ensure_artefacts_path",
    "get_array_atomic_type",
    "get_dict_atomic_types",
    "get_sanitized_schema_type",
]
