"""Includes consts for use in the sync modulde."""

from os import getenv
from pathlib import Path
from re import DOTALL, MULTILINE
from re import compile as re_compile

from dotenv import load_dotenv

load_dotenv()

ONEPLAN_API_HOST = "eu.oneplan.ai"
ONEPLAN_API_URL_BASE = f"https://{ONEPLAN_API_HOST}"
ONEPLAN_API_URL_HELP_BASE = f"{ONEPLAN_API_URL_BASE}/ApiHelp"
ONEPLAN_API_BROKEN_PATHS = ("POST-api-resources-id-syncphoto_BlankPhoto",)

MARKER_PAGE_ERROR = "<title>Error</title>"
MARKER_ANCHOR_MODEL = '<a href="/ApiHelp/ResourceModel?modelName='
MARKER_ENUMERATION = "enumeration values"
MARKER_TYPE_COLLECTION = "Collection of "
MARKER_TYPE_DICTIONARY = "Dictionary of "
MARKER_DEFAULT_VALUE = "Default value is "

DEFAULT_REQUEST_SLEEP_SECONDS = 1.0

PATH_REPO = Path(__file__).parents[2]
PATH_CACHE = PATH_REPO / "cache"
PATH_ONEPLAN_API_DOCS = PATH_CACHE / "oneplan_api_docs.html"
PATH_DB = PATH_CACHE / "db"

PATH_ARTEFACTS = PATH_REPO / "artefacts"
PATH_ARTEFACTS_SPEC = PATH_ARTEFACTS / "api.yaml"
PATH_ARTEFACTS_CLIENT_ZIP = PATH_ARTEFACTS / "client.zip"
PATH_ARTEFACTS_CLIENT = PATH_ARTEFACTS / "client"

PATH_CLIENT = PATH_REPO / "oneplan_sdk" / "client"

RE_API_ENDPOINT = re_compile(
    r'<a href="/ApiHelp/Api/([^"]+)">(POST|GET|PATCH|PUT|DELETE) ([^<]+)</a>',
    DOTALL | MULTILINE,
)
RE_API_GROUP = re_compile(r"api/([^/\?]+).?")
RE_DICTIONARY_TYPE_PARTS = re_compile(
    r"Dictionary of (.*?) \[key\] and (.*) \[value\]", DOTALL | MULTILINE
)
RE_MODEL_URL = re_compile(r"/ApiHelp/ResourceModel.*")
RE_URL_PARAMS = re_compile(r"{(.*?)}", DOTALL)
RE_SPACES = re_compile(r"\s+")

REQUEST_HEADERS: dict[str, str] = {
    "Host": ONEPLAN_API_HOST,
    "User-Agent": getenv("USER_AGENT"),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "TE": "trailers",
    "Cookie": getenv("ASPNET_COOKIE"),
}

SCHEMA_REF_PREFIX = "#/components/schemas/"
SECURITY_SCHEME_NAME = "oneplan_api_auth"
URL_CLIENT_GEN = "https://generator3.swagger.io/api/generate"
