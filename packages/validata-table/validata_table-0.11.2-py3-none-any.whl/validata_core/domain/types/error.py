import pprint
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import frictionless
import frictionless.fields as frfields
from frictionless import errors as frerrors

from validata_core.domain.types.schema import Schema

Title = str
Message = str
ErrTxt = Tuple[Title, Message]


class Error:
    def __init__(self, error: frictionless.Error):
        self.frless_error: frictionless.Error = error

        # All following attributes are deprecated in frictionless
        # but kept in this class for retrocompatibility

        self.code: str = error.type
        self.name: str = ""

        # Init Error object with frictionless.CellError object's properties
        if isinstance(error, frerrors.CellError):
            self.field_position: int = error.field_number
            self.row_position: int = error.row_number

        # Init Error object with frictionless.LabelError object's properties
        if isinstance(error, frerrors.LabelError):
            self.field_position: int = error.field_number
            self.row_positions: List[int] = error.row_numbers

        # Init Error object with frictionless.RowError object's properties
        if isinstance(error, frerrors.RowError):
            self.row_position: int = error.row_number

    def set_translation(self, translation: ErrTxt):
        title = translation[0]
        message = translation[1]
        if title != "":
            self.title = title
        if message != "":
            self.message = message

    @property
    def type(self) -> str:
        return self.frless_error.type

    @property
    def title(self) -> str:
        return self.frless_error.title

    @title.setter
    def title(self, value: str):
        self.frless_error.__setattr__("title", value)

    @property
    def description(self) -> str:
        return self.frless_error.description

    @property
    def message(self) -> str:
        return self.frless_error.message

    @message.setter
    def message(self, value: str):
        self.frless_error.message = value

    @property
    def note(self) -> str:
        return self.frless_error.note

    def __repr__(self) -> str:
        """Overwrites frictionless.metadata __repr__ method to use overwritten 'to_dict()' method.
        Returns a dict representation of Error object
        """
        return pprint.pformat(self.to_dict(), sort_dicts=True)

    def to_dict(self, frless_dict: Optional[Dict] = None) -> Dict[str, Any]:
        """Overwrites frictionless.metadata to_dict() method.
        Returns a dict containing all Error object's properties information with added
        some deprecated information linked to this error.
        """

        if not frless_dict:
            dict_error = self.frless_error.to_dict()
        else:
            dict_error = frless_dict

        # All following key-values are deprecated in frictionless
        # but kept in this class for retrocompatibility
        dict_error["code"] = self.code
        dict_error["name"] = self.name

        if "fieldNumber" in dict_error.keys():
            dict_error["fieldPosition"] = dict_error["fieldNumber"]

        if "rowNumber" in dict_error.keys():
            dict_error["rowPosition"] = dict_error["rowNumber"]

        if "rowNumbers" in dict_error.keys():
            dict_error["rowPositions"] = dict_error["rowNumbers"]

        return dict_error


class ConstraintError(Error):
    """An error occured while validating a specific cell

    Additional context is stored
    """

    def __init__(self, error: frerrors.ConstraintError, schema: Optional[Schema]):
        super().__init__(error)
        err = error
        field_name = err.field_name

        self.field_def: Optional[frictionless.Field] = (
            schema.find_field_in_schema(field_name) if schema else None
        )

        self.violated_constraint: Optional[str] = _extract_constraint_from_message(err)
        self.cell_value = err.cell

    def get_constraint_value(
        self,
    ) -> Any:
        """Extract and return constraint value from a field constraints"""

        if not self.violated_constraint or not self.field_def:
            return ""

        is_array_field = isinstance(self.field_def, frfields.array.ArrayField)

        if is_array_field:
            assert isinstance(self.field_def, frfields.array.ArrayField)
            assert self.field_def.array_item is not None
            return self.field_def.array_item["constraints"][self.violated_constraint]

        else:
            return self.field_def.constraints[self.violated_constraint]


CONSTRAINT_RE = re.compile(r'^constraint "([^"]+)" is .*$')
ARRAY_CONSTRAINT_RE = re.compile(r'^array item constraint "([^"]+)" is .*$')


def _extract_constraint_from_message(err: frerrors.Error) -> Optional[str]:
    m = CONSTRAINT_RE.match(err.note) or ARRAY_CONSTRAINT_RE.match(err.note)

    return m[1] if m else None


@dataclass
class ValidataSourceError(Exception):
    name: str
    message: str


@dataclass
class FileExtensionError(Exception):
    name: str
    message: str


class CustomCheckError(Error):
    def __init__(self, note: str):
        class FrlessCustomCheckError(frerrors.ResourceError):
            type = "format-error"
            title = "Format Error"
            description = "Data reading error because of incorrect format."
            template = "The data source could not be successfully parsed: {note}"

        frerr = FrlessCustomCheckError(note=note)
        return super().__init__(frerr)
