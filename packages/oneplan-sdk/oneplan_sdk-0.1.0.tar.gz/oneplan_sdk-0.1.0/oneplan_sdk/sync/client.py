"""Includes functionality to autogenerate the python client from the OpenApi 3.0 spec."""

from collections.abc import Iterator, Sequence
from dataclasses import asdict
from json import dumps as json_dumps
from os import getenv
from pathlib import Path
from shutil import copy as file_copy
from shutil import copytree, rmtree
from zipfile import ZipFile

from requests import post

from oneplan_sdk.sync.consts import (
    PATH_ARTEFACTS_CLIENT,
    PATH_ARTEFACTS_CLIENT_ZIP,
    PATH_ARTEFACTS_SPEC,
    PATH_CLIENT,
    URL_CLIENT_GEN,
)
from oneplan_sdk.sync.spec import OpenApiSpec
from oneplan_sdk.sync.util import ensure_client_path


def generate_python_client(spec: OpenApiSpec, force_regen: bool = False) -> None:
    """Downloads the python client for the API using the authoritative OpenAPI generator."""
    if PATH_ARTEFACTS_CLIENT_ZIP.exists() and not force_regen:
        return

    data = dict(spec=asdict(spec), lang="python", type="CLIENT")

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Length": "221829",
        "Content-Type": "application/json",
        "Dnt": "1",
        "Origin": "https://editor-next.swagger.io",
        "Priority": "u=1, i",
        "Referer": "https://editor-next.swagger.io/",
        "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": getenv("USER_AGENT"),
    }

    with post(
        URL_CLIENT_GEN, data=json_dumps(data), headers=headers, timeout=60.0
    ) as res:
        if res.status_code < 400:
            with open(PATH_ARTEFACTS_CLIENT_ZIP, "wb") as f:
                f.write(res.content)


def add_client_artefacts_to_package() -> None:
    """Copies over the relevant client artefacts to the oneplan_sdk package."""
    with ZipFile(PATH_ARTEFACTS_CLIENT_ZIP, "r") as z:
        z.extractall(PATH_ARTEFACTS_CLIENT)

    ensure_client_path()

    for folder in ("swagger_client", "docs"):
        target_path = PATH_CLIENT / folder

        if target_path.exists():
            rmtree(target_path)

        copytree(PATH_ARTEFACTS_CLIENT / folder, target_path)

    file_copy(PATH_ARTEFACTS_CLIENT / "README.md", PATH_CLIENT)
    file_copy(PATH_ARTEFACTS_SPEC, PATH_CLIENT)


def parse_client_folder(extensions: Sequence[str]) -> Iterator[Path]:
    """Returns an iterator over SDK client folder files of interest."""
    extensions = tuple(extensions)

    for path in PATH_CLIENT.rglob("*"):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def replace_text_in_file(path: Path, search: str, replace: str) -> None:
    """Substitutes replace text for search text in a file located at the path."""
    with open(path, "rt") as f:
        text = f.read()

    text = text.replace(search, replace)

    with open(path, "wt") as f:
        f.write(text)


def sanitize_client_files() -> None:
    """Sanitizes python files, docs files and the README in the SDK client folder."""
    for path in parse_client_folder(extensions=[".md", ".py"]):
        replace_text_in_file(
            path, "swagger_client", "oneplan_sdk.client.swagger_client"
        )

    path = PATH_CLIENT / "README.md"

    with open(path, "rt") as f:
        readme = f.read()

    beg = readme.find("## Requirements.")
    end = readme.find("## Getting Started")

    readme = readme[:beg] + readme[end:]

    with open(path, "wt") as f:
        f.write(readme)


__all__ = [
    "generate_python_client",
    "add_client_artefacts_to_package",
    "sanitize_client_files",
]
