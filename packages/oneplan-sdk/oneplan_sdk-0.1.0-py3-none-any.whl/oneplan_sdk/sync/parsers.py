"""Includes html document parsers for the OnePlan API docs."""

from collections.abc import Iterator

from bs4 import BeautifulSoup, Tag

from oneplan_sdk.sync.interfaces import (
    IApiEnumeration,
    IApiEnumerationMember,
    IApiModel,
    IApiModelField,
    IApiModelMeta,
)


def get_model_url_path(soup: BeautifulSoup, header: str) -> IApiModelMeta | None:
    """Returns the url path to an object model in the OnePlan API.

    The model is linked to from the first anchor after the headers
    Request Information -> Body Parameters, or
    Response Information -> Resource Description.
    If there is no request or response body, this will return None.

    Note that further models can be embedded inside a model,
    and discovering those is the responsibility of a separate recursive method.
    """
    anchor = soup.find("body").find_next("h3", string=header).find_next(["a", "h2"])

    if anchor and "href" in anchor.attrs:
        return IApiModelMeta(anchor.attrs.get("href"))


def parse_model__or_enumeration_table(
    table: Tag,
    model: IApiModelMeta | None,
    is_enumeration: bool,
    has_header: bool = True,
) -> IApiModel | IApiEnumeration | None:
    """Returns an instance of IApiModel that captures the model attributes."""

    def get_table_rows() -> Tag:
        offset = int(has_header)
        return table.find_all("tr")[offset:]

    def get_row_values(row: Tag) -> Iterator[str]:
        return (td.text.strip() for td in row.find_all("td"))

    if is_enumeration:
        object_class = IApiEnumeration
        field_class = IApiEnumerationMember
    else:
        object_class = IApiModel
        field_class = IApiModelField

    return object_class(
        name=model.model_name if model else None,
        fields=tuple(field_class(*get_row_values(row)) for row in get_table_rows()),
    )


def parse_model_table(
    table: Tag, model: IApiModelMeta | None = None, has_header: bool = True
) -> IApiModel | None:
    """Returns an instance of IApiModel that captures the model fields."""
    return parse_model__or_enumeration_table(
        table, model, is_enumeration=False, has_header=has_header
    )


def parse_enumeration_table(
    table: Tag, model: IApiModelMeta | None = None, has_header: bool = True
) -> IApiEnumeration | None:
    """Returns an instance of IApiEnumeration that captures the enumeration members."""
    return parse_model__or_enumeration_table(
        table, model, is_enumeration=True, has_header=has_header
    )


__all__ = ["get_model_url_path", "parse_model_table", "parse_enumeration_table"]
