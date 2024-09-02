from typing import Protocol as _Protocol, runtime_checkable as _runtime_checkable, Any

from pyprotocol import Stringable


@_runtime_checkable
class HTMLCode(_Protocol):
    """An object representing HTML code."""

    _IS_HTML_CODE: Any

    def str(self, indent: int) -> str:
        ...


@_runtime_checkable
class MDCode(_Protocol):
    """An object representing Markdown code."""

    _IS_MD_CODE: Any

    def __str__(self) -> str:
        ...


ContentType = Stringable | HTMLCode | MDCode
ContentInputType = (
    dict[str | int, ContentType]
    | list[ContentType]
    | tuple[ContentType]
    | None
)

AttrsType = dict[str, Stringable | bool]
