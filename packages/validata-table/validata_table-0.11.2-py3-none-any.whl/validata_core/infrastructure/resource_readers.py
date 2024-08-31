import json
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple, Union

import frictionless
from frictionless import formats
from frictionless.resources import TableResource

from validata_core.domain.spi import (
    FileContentService,
    InlineContentService,
    LocalContentFetcher,
    RemoteFileService,
    RequestService,
)
from validata_core.domain.types import (
    Error,
    FileExtensionError,
    Header,
    InlineData,
    Row,
    SchemaDescriptor,
    ValidataSourceError,
)
from validata_core.domain.types.utils import Res


def _extract_header_and_rows_from_resource(
    resource: TableResource,
) -> Tuple[Header, List[Row]]:
    """Extract header and data rows from frictionless source and options."""

    try:
        with resource as open_resource:
            if open_resource.cell_stream is None:
                raise ValueError("impossible de lire le contenu")

            lines: List[Sequence[Any]] = list(open_resource.read_cells())

            if not lines:
                raise ValueError("contenu vide")

            header: Header = lines[0]
            rows: List[Row] = lines[1:]

            # Fix BOM issue on first field name
            BOM_UTF8 = "\ufeff"

            if header and header[0].startswith(BOM_UTF8):
                header: Header = [header[0].replace(BOM_UTF8, "")] + list(header[1:])

        return header, rows

    except ValueError as value_error:
        raise ValidataSourceError(
            name="source-error",
            message=value_error.args[0],
        ) from value_error

    except frictionless.exception.FrictionlessException as exception:
        validata_error = Error(exception.error)
        raise ValidataSourceError(
            name=validata_error.title,
            message=validata_error.message,
        ) from exception


class FrictionlessFileContentService(FileContentService):
    def read_header_and_rows(
        self, filename: str, content: bytes
    ) -> Tuple[Header, List[Row]]:
        table_resource = self._to_frictionless(filename, content)
        return _extract_header_and_rows_from_resource(table_resource)

    def _to_frictionless(self, filename: str, content: bytes) -> TableResource:
        """Uploaded file implementation"""
        file_ext = Path(filename).suffix.lower()

        format = self._detect_format_from_file_extension(file_ext)
        options = {
            "format": format,
            "detector": frictionless.Detector(encoding_function=_detect_encoding),
            **_control_option(format),
        }
        if format in {"csv", "tsv"}:
            options["encoding"] = _detect_encoding(content)
        source = content

        return TableResource(source, **options)

    @staticmethod
    def _detect_format_from_file_extension(file_ext: str):
        if file_ext in (".csv", ".tsv", ".ods", ".xls", ".xlsx"):
            return file_ext[1:]
        else:
            raise FileExtensionError(
                name="file_extension_error",
                message=f"This file extension {file_ext} is not yet supported",
            )


class FrictionlessRemoteFileService(RemoteFileService):
    def __init__(self, request_service: RequestService):
        self._request_service = request_service

    def read_header_and_rows(self, url: str) -> Tuple[Header, List[Row]]:
        table_resource = self._to_frictionless(url)
        return _extract_header_and_rows_from_resource(table_resource)

    def _to_frictionless(self, url: str) -> TableResource:
        """URL implementation"""
        suffix = Path(url).suffix
        format = (
            suffix[1:]
            if suffix.startswith(".")
            else self._guess_format_from_content_type(url)
        )

        return TableResource(
            url,
            **{
                "detector": frictionless.Detector(encoding_function=_detect_encoding),
                **_control_option(format),
                "format": format,
            },
        )

    def _guess_format_from_content_type(self, url: str) -> str:
        content_type: Optional[str] = self._request_service.get_content_type_header(url)
        default = "csv"

        if content_type is None:
            return default

        if content_type.startswith("text/csv"):
            return "csv"

        elif content_type.startswith("application/vnd.ms-excel"):
            return "xls"

        elif content_type.startswith("application/vnd.openxmlformats"):
            return "xlsx"

        return default


def _control_option(format: str) -> dict:
    # In Frictionless v5  ExcelFormat dialect is replaced by ExcelControl format,
    # see https://framework.frictionlessdata.io/docs/formats/excel.html for more information
    return (
        {"control": formats.ExcelControl(preserve_formatting=True)}
        if format == "xlsx"
        else {}
    )


def _detect_encoding(buffer: bytes) -> str:
    """Try to decode using utf-8 first, fallback on frictionless helper function."""
    try:
        buffer.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        encoding = frictionless.Detector().detect_encoding(buffer)
        return encoding.lower()


class FrictionlessInlineContentService(InlineContentService):
    def read_header_and_rows(self, data: InlineData) -> Tuple[Header, List[Row]]:
        frless_resource = self._to_frictionless(data)
        return _extract_header_and_rows_from_resource(frless_resource)

    def _to_frictionless(self, data: InlineData) -> TableResource:
        return TableResource(data)


class LocalContentReader(LocalContentFetcher):
    def fetch(self, filepath: Union[str, Path]) -> Res[SchemaDescriptor, Error]:
        with open(filepath) as f:
            content = f.read()
        schema_descriptor: SchemaDescriptor = json.loads(content)
        return schema_descriptor, None
