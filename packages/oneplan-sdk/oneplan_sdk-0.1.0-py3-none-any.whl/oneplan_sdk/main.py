"""Includes the main interface for the auto-generated OnePlan API client SDK.

The auto-generated client already provides excellent documentation
and straightforward code samples for each individual endpoint in the API.

However, this module provides an even more simplified higher-level interdface,
which abstracts any repetitive configuration logic
and allows developers to invoke API requests with minimal code.
"""

from collections.abc import Callable
from importlib import import_module
from inspect import getmembers, isclass
from os import getenv
from typing import Any
from dotenv import load_dotenv
from oneplan_sdk.client.swagger_client import ApiClient, Configuration

CLIENT_API_MODULE_NAME = "oneplan_sdk.client.swagger_client.api"
CLIENT_API_MEMBERS: dict[str, type] = {
    member.__module__: member
    for _, member in getmembers(import_module(CLIENT_API_MODULE_NAME))
    if isclass(member)
    and member.__module__.startswith(CLIENT_API_MODULE_NAME)
}


def get_configured_api_client() -> ApiClient:
    """Returns a configured OnePlan API client."""
    load_dotenv()

    config = Configuration()
    config.username = getenv("ONEPLAN_API_USERNAME")
    config.password = getenv("ONEPLAN_API_PASSWORD")

    return ApiClient(configuration=config)


def make_request(method: Callable, *args, **kwargs) -> Any:
    """Returns the repsonse body of an api requets, if successful."""
    api_client = get_configured_api_client()
    api = CLIENT_API_MEMBERS[method.__module__]
    api_instance = api(api_client)
    api_method = getattr(api_instance, method.__name__)
    return api_method(*args, **kwargs)


__all__ = ["get_configured_api_client", "make_request"]
