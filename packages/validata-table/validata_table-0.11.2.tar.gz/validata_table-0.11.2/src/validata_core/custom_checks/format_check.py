from typing import Any, Dict, Iterable, List, Optional

import attrs
from frictionless import Check, Row
from frictionless.errors import CellError, Error

from validata_core.domain.types import Validator


class FormatCheck:
    """A FormatCheck is a check that can evaluate a single value without
    needing any more context.

    Options can be passed as parameters
    """

    def __init__(
        self,
        format_validator: Validator,
        format_code: str,
        err_title: str,
        err_description: str,
        err_msg_template: str,
        available_options: List[str] = [],
    ):
        self._format_validator = format_validator
        self._format_code = format_code
        self._err_title = err_title
        self._err_description = err_description
        self._err_msg_template = err_msg_template
        self._available_options = available_options

    def from_descriptor(self, descriptor) -> Check:
        """This temporary method bridges the gap between frictionless checks
        and FormatCheck, as long as both are used side-by-side.

        It will eventually be phased out.
        """
        fieldname = descriptor["column"]
        options = {k: v for (k, v) in descriptor.items() if k != "column"}
        return self.to_frictionless_check(fieldname, **options)

    def to_frictionless_check(self_format_check, fieldname: str, **kwargs) -> Check:  # type: ignore[reportSelfClsParameterName]
        _metadata_profile = {  # type: ignore
            "type": "object",
            "required": ["column"],
            "properties": {"column": {"type": "string"}},
        }

        if self_format_check._available_options:
            _metadata_profile["properties"]["options"] = {
                "type": "object",
                "properties": {},
            }

            for option in self_format_check._available_options:
                _metadata_profile["properties"]["options"]["properties"][option] = {
                    "type": ["boolean", "string", "number", "object", "array"]
                }

        class CustomFormatError(CellError):
            type = self_format_check._format_code
            name = self_format_check._err_title
            title = self_format_check._err_title
            tags = ["#body"]
            template = self_format_check._err_msg_template
            description = self_format_check._err_description

        @attrs.define(kw_only=True, repr=False)
        class NewCheck(Check):
            column: str = ""
            options: Dict[str, Any] = {}
            type = self_format_check._format_code
            Errors = [CustomFormatError]

            def validate_start(self) -> Iterable[Error]:
                return []

            def validate_row(self, row: Row) -> Iterable[Error]:
                cell_value = row[self.column]

                # Empty cell, don't check!
                if not cell_value:
                    return []
                else:
                    yield from self._validate_row(cell_value, row)

            def _validate_row(self, cell_value: Any, row: Row) -> Iterable[Error]:
                is_valid, note = self_format_check._format_validator(
                    cell_value, **self.options
                )

                if not is_valid:
                    err = CustomFormatError.from_row(
                        row, note=note, field_name=self.column
                    )
                    yield err

                return

            metadata_profile = _metadata_profile

            @classmethod
            def metadata_select_class(cls, type: Optional[str]):
                return cls

        if kwargs:
            descriptor = {"options": kwargs, "column": fieldname}
        else:
            descriptor = {"column": fieldname}

        return NewCheck.from_descriptor(descriptor)
