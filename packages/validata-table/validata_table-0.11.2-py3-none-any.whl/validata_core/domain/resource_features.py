from pathlib import Path
from typing import Any, Dict, Union

from validata_core.domain.helpers import FileContentReader, InlineReader, URLReader
from validata_core.domain.spi import (
    FileContentService,
    InlineContentService,
    RemoteFileService,
    ToDictService,
)
from validata_core.domain.types import InlineData, Report, Source, ValidataResource


class ResourceFeatures:
    def __init__(
        self,
        file_content_service: FileContentService,
        remote_file_service: RemoteFileService,
        inline_content_service: InlineContentService,
        to_dict_service: ToDictService,
    ):
        self._file_content_service = file_content_service
        self._remote_file_service = remote_file_service
        self._to_dict_service = to_dict_service
        self._inline_content_service = inline_content_service

    def from_file_content(
        self, filename: Union[str, Path], content: bytes
    ) -> ValidataResource:
        return ValidataResource(
            FileContentReader(filename, content, self._file_content_service)
        )

    def from_remote_file(self, url: str) -> ValidataResource:
        return ValidataResource(URLReader(url, self._remote_file_service))

    def from_inline_data(self, data: InlineData) -> ValidataResource:
        return ValidataResource(InlineReader(data, self._inline_content_service))

    def to_dict(self, report: Report) -> Dict[str, Any]:
        return self._to_dict_service.report_to_dict(report)

    def make_validata_resource(self, source: Source) -> ValidataResource:
        if not isinstance(source, str) and not isinstance(source, Path):
            return self.from_inline_data(source)

        if isinstance(source, str) and source.startswith("http"):
            url = source
            return self.from_remote_file(url)
        else:
            path = source
            with open(path, "rb") as f:
                content: bytes = f.read()
            return self.from_file_content(path, content)
