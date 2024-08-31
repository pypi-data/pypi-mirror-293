from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Tuple, Union

from frictionless import Check

from validata_core.domain.types import (
    Error,
    Header,
    InlineData,
    Report,
    Row,
    Schema,
    SchemaDescriptor,
    ValidataResource,
    Validator,
)
from validata_core.domain.types.utils import Res


class ValidationService(Protocol):
    def validate(
        self,
        resource: ValidataResource,
        schema: Schema,
        checks: List[Check],
        header_case_sensitive: bool,
    ) -> Report:
        ...

    def validate_schema(
        self, schema_descriptor: Union[SchemaDescriptor, str, Path]
    ) -> Report:
        ...


class RequestService(Protocol):
    def get_content_type_header(self, url: str) -> Optional[str]:
        ...


class FileContentService(Protocol):
    def read_header_and_rows(
        self, filename: str, content: bytes
    ) -> Tuple[Header, List[Row]]:
        ...


class InlineContentService(Protocol):
    def read_header_and_rows(self, data: InlineData) -> Tuple[Header, List[Row]]:
        ...


class RemoteFileService(Protocol):
    def read_header_and_rows(self, url: str) -> Tuple[Header, List[Row]]:
        ...


class ToDictService(Protocol):
    # Not very elegant, but encapsulates the current dependency to
    # frictionless for the conversion
    def report_to_dict(self, report: Report) -> Dict[str, Any]:
        ...


class TableSchemaService(Protocol):
    """Service provider interface for dealing with table schema specification"""

    def parse(self, descriptor: SchemaDescriptor) -> Res[Schema, Error]:
        """Parses a standard table schema descriptor into a Schema object

        All specificities of the profile (as opposed to the standard
        specification) are ignored
        """
        ...


class RemoteContentFetcher(Protocol):
    def fetch(self, url: str) -> Res[SchemaDescriptor, Error]:
        ...


class LocalContentFetcher(Protocol):
    def fetch(self, filepath: Union[str, Path]) -> Res[SchemaDescriptor, Error]:
        ...


class CustomFormatsRepository(Protocol):
    def ls(self) -> List[str]:
        """Returns a list of valid formats"""
        ...

    def get_validator(self, format: str) -> Validator:
        """Returns a validator function for the format

        Should not raise an error for an invalid format. Return `lambda x:
        True` instead"""
        ...

    def get_description(self, format: str) -> str:
        """Returns a description of the format

        Should not raise an error for an invalid format. Return an empty
        string instead"""
        ...
