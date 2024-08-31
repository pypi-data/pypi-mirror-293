import logging
from pathlib import Path
from typing import Dict, List, Sequence, Tuple, Union

from frictionless import errors as frerrors

from validata_core.domain.spi import (
    FileContentService,
    InlineContentService,
    RemoteFileService,
)
from validata_core.domain.types import Header, InlineData, Row, TableReader

log = logging.Logger(__name__)


class FileContentReader(TableReader):
    def __init__(
        self, filename: Union[str, Path], content: bytes, service: FileContentService
    ):
        self._filename = str(filename)
        self._content = content
        self._service = service

    def source(self) -> str:
        return self._filename

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        return self._service.read_header_and_rows(self._filename, self._content)


class URLReader(TableReader):
    def __init__(self, url: str, service: RemoteFileService):
        self._url = url
        self._service = service

    def source(self) -> str:
        return self._url

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        return self._service.read_header_and_rows(self._url)


class InlineReader(TableReader):
    def __init__(self, data: InlineData, service: InlineContentService):
        self._data = data
        self._service = service

    def source(self) -> str:
        return "inline"

    def read_header_and_rows(self) -> Tuple[Header, List[Row]]:
        return self._service.read_header_and_rows(self._data)


BODY_TAGS = frozenset(["#body", "#cell", "#content", "#row", "#table"])
STRUCTURE_TAGS = frozenset(["#head", "#structure", "#header"])


def is_body_error(err: Union[frerrors.Error, Dict]) -> bool:
    """Classify the given error as 'body error' according to its tags."""
    tags = err.tags if isinstance(err, frerrors.Error) else err["tags"]
    return bool(BODY_TAGS & set(tags))


def is_structure_error(err: Union[frerrors.Error, Dict]) -> bool:
    """Classify the given error as 'structure error' according to its tags."""
    tags = err.tags if isinstance(err, frerrors.Error) else err["tags"]
    return bool(STRUCTURE_TAGS & set(tags))


def to_lower(str_array: Sequence[str]) -> List[str]:
    """Lower all the strings in a list"""
    return [s.lower() for s in str_array]
