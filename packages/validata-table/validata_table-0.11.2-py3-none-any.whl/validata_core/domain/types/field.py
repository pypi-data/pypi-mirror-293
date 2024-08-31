from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import frictionless


@dataclass
class FrFormatObj:
    name: str
    options: Dict[str, Any]


FrFormat = Union[str, FrFormatObj]


class Field:
    def __init__(self, field: frictionless.Field):
        self.frless_field = field

    @property
    def fr_format(self) -> Optional[FrFormat]:
        descriptor = self.frless_field.to_descriptor()
        if "frFormat" not in descriptor:
            return None

        fr_format_descriptor = descriptor["frFormat"]

        if isinstance(fr_format_descriptor, str):
            return fr_format_descriptor

        else:
            return FrFormatObj(
                fr_format_descriptor["name"],
                {k: v for k, v in fr_format_descriptor.items() if k != "name"},
            )

    @property
    def name(self) -> str:
        return self.frless_field.name
