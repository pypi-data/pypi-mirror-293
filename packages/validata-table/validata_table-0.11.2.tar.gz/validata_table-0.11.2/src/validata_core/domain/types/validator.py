from typing import Protocol, Tuple

from .json import JSON

# ValidationDetails allow to optionnaly return specific validation messages with
# the validation result.
ValidationNote = str
ValidationResult = Tuple[bool, ValidationNote]


class Validator(Protocol):
    """A Validator is a function that takes a value and returns if is value
    is valid or not, along with a note that can give hints about the validation result.

    The note can be an empty string.

    Additional options can be provided, however sensible defaults should be
    chosen so that the Validator does not fail if no option is provided.
    """

    def __call__(self, value: str, **options: JSON) -> ValidationResult:
        ...
