"""Includes utility methods for retrieving, caching, syncing and reading OnePlan API docs pages."""

from collections.abc import Iterator
from pathlib import Path
from time import sleep
from typing import Optional

from bs4 import BeautifulSoup
from requests import Session

from oneplan_sdk.sync.consts import (
    DEFAULT_REQUEST_SLEEP_SECONDS,
    MARKER_PAGE_ERROR,
    ONEPLAN_API_BROKEN_PATHS,
    ONEPLAN_API_URL_HELP_BASE,
    PATH_CACHE,
    PATH_ONEPLAN_API_DOCS,
    RE_API_ENDPOINT,
    RE_MODEL_URL,
    REQUEST_HEADERS,
)
from oneplan_sdk.sync.interfaces import IApiModelMeta, IDocMeta
from oneplan_sdk.sync.parsers import get_model_url_path
from oneplan_sdk.sync.util import ensure_cache_path


def local_doc_exists(path: Path) -> bool:
    """Returns True if a cache file path exists."""
    return path.exists()


def read_local_doc(path: Path) -> str | None:
    """Returns the text of the version of docs in the local cache."""
    if local_doc_exists(path):
        with open(path, "rt") as f:
            return f.read()


def get_session() -> Session:
    """Returns a session for crawling the doc pages."""
    session = Session()
    session.headers.update(REQUEST_HEADERS)

    return session


def fetch_remote_doc(
    url: str,
    session: Session,
    referer: Optional[str] = None,
    sleep_seconds: float = DEFAULT_REQUEST_SLEEP_SECONDS,
) -> str | None:
    """Returns the text of the Oneplan API Help docs page."""
    if referer is not None:
        session.headers["Referer"] = referer

    with session.get(url, timeout=3) as res:
        sleep(sleep_seconds)
        if res.status_code < 400:
            return res.text


def list_docs_info() -> Iterator[IDocMeta]:
    """Returns an iterator over meta info for all endpoint doc pages."""
    docs = read_local_doc(PATH_ONEPLAN_API_DOCS)
    return (IDocMeta(*match) for match in RE_API_ENDPOINT.findall(docs))


def sync_doc(
    url: str, local_path: str, session: Session, referer: Optional[str] = None
) -> bool:
    """Returns True if locally cached docs were refreshed with updated Oneplan API docs."""
    if local_doc_exists(local_path):
        return False

    doc = fetch_remote_doc(url, session, referer=referer)

    if doc is None or MARKER_PAGE_ERROR in doc:
        return False

    with open(local_path, "wt") as f:
        f.write(doc)

    return True


def sync_docs(full_refresh: bool = False) -> None:
    """Fully re-syncs all OnePlan API docs with the local cache."""
    ensure_cache_path()
    session = get_session()
    sync_doc(ONEPLAN_API_URL_HELP_BASE, PATH_ONEPLAN_API_DOCS, session)

    for doc in list_docs_info():
        if local_doc_exists(doc.local_path) and not full_refresh:
            continue

        sync_doc(doc.url, doc.local_path, session)


def sync_model(
    model: IApiModelMeta,
    session: Session,
    referer_url: str,
    ignored_model_names: set | None = None,
) -> None:
    """Synchronizes the docs for an individual API Model."""
    if ignored_model_names is None:
        ignored_model_names = set()

    if model.model_name in ignored_model_names:
        return

    ignored_model_names.add(model.model_name)

    if not local_doc_exists(model.local_path):
        refreshed = sync_doc(model.url, model.local_path, session, referer=referer_url)
        if not refreshed:
            print(model.model_name, len(ignored_model_names), referer_url)

    inspect_model(model, session, ignored_model_names)


def inspect_model(
    model: IApiModelMeta,
    session: Session,
    ignored_model_names: set | None = None,
) -> None:
    if not local_doc_exists(model.local_path):
        return

    with open(model.local_path, "rt") as f:
        doc = f.read()

    anchors = (
        BeautifulSoup(doc, "html.parser").find("body").find_all("a", href=RE_MODEL_URL)
    )
    nested_models = [IApiModelMeta(anchor.get("href")) for anchor in anchors]

    for nested_model in nested_models:
        sync_model(
            nested_model, session, model.url, ignored_model_names=ignored_model_names
        )


def sync_models() -> None:
    """Synchronizes the request/responce API models for all endpoints."""
    session = get_session()
    ignored_model_names = set()

    for doc in list_docs_info():
        if doc.url_path in ONEPLAN_API_BROKEN_PATHS:
            continue

        page = read_local_doc(doc.local_path)

        soup = BeautifulSoup(page, "html.parser")

        for header in ("Body Parameters", "Resource Description"):
            model = get_model_url_path(soup, header)

            if model:
                sync_model(
                    model,
                    session,
                    doc.url,
                    ignored_model_names,
                )


def list_local_models() -> Iterator[IApiModelMeta]:
    """Returns an iterator over the paths to locally cached Api models."""
    return (
        IApiModelMeta.from_local_path(path)
        for path in PATH_CACHE.iterdir()
        if path.stem.startswith("MODEL-")
    )


__all__ = [
    "read_local_doc",
    "list_docs_info",
    "sync_docs",
    "sync_models",
    "list_local_models",
]
