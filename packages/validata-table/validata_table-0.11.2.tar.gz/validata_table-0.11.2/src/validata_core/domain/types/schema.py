from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import frictionless

from validata_core.domain.types.field import Field
from validata_core.domain.types.json import JSON

SchemaDescriptor = Dict[str, JSON]


@dataclass
class CustomCheck:
    name: str
    params: Dict[str, JSON]


@dataclass
class Schema:
    descriptor: SchemaDescriptor
    fields: List[Field]
    custom_checks: List[CustomCheck]

    def get_custom_checks(self) -> List[CustomCheck]:
        return self.custom_checks

    def get_fields(self) -> List[Field]:
        return self.fields

    def find_field_in_schema(self, field_name: str) -> Optional[frictionless.Field]:
        return next(
            (field.frless_field for field in self.fields if field.name == field_name),
            None,
        )
