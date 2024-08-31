"""
    Year Interval Value check

    Vérifie que l'on a bien une valeur du type "aaaa/aaaa" avec la première année
    inférieure à la seconde ou une année seulement
    (si le paramètre allow-year-only est activé)

    Messages d'erreur attendus :
    - Si la valeur n'est pas du type ^\\d{4}/\\d{4}$ (ex : "toto")
      - La valeur "toto" n'a pas le format attendu pour une période (AAAA/AAAA).
    - Si les deux années sont identiques (ex : "2017/2017")
      - Période "2017/2017 invalide. Les deux années doivent être différentes).
    - Si la deuxième année est inférieure à la première (ex : "2017/2012")
      - Période "2017/2012" invalide. La deuxième année doit être postérieure
        à la première (2012/2017).

    Pierre Dittgen, Jailbreak
"""
import re
from typing import Any, Iterable, Optional, Type, Union

import attrs
from frictionless import Row, errors, types
from typing_extensions import Self

from .utils import CustomCheckSingleColumn

YEAR_INTERVAL_RE = re.compile(r"^(\d{4})/(\d{4})$")
YEAR_RE = re.compile(r"^\d{4}$")

# Module API


class YearIntervalValueError(errors.CellError):
    """Custom error."""

    type = "year-interval-value"
    name = "Année ou intervalle d'années"
    title = name
    tags = ["#body"]
    template = "L'année ou l'intervalle d'année '{cell}' est incorrect ({note})."
    description = "Année ou intervalle d'années"


@attrs.define(kw_only=True, repr=False)
class YearIntervalValue(CustomCheckSingleColumn):
    """Year Interval Value check class."""

    type = "year-interval-value"
    allow_year_only: bool = False

    Errors = [YearIntervalValueError]

    @classmethod
    def from_descriptor(cls, descriptor: Union[str, types.IDescriptor]) -> Self:
        if isinstance(descriptor, dict) and "allow-year-only" in descriptor.keys():
            cls.allow_year_only = descriptor["allow-year-only"] in ("true", "yes")
        else:
            cls.allow_year_only = False
        return super().from_descriptor(descriptor)

    def _validate_start(self) -> Iterable[errors.Error]:
        return []

    def _validate_row(self, cell_value: Any, row: Row) -> Iterable[errors.Error]:
        # Checks for interval format
        rm = YEAR_INTERVAL_RE.match(cell_value)
        if not rm:
            # Not an interval, is this a year only?
            if self.allow_year_only:
                ym = YEAR_RE.match(cell_value)

                # No -> add error
                if not ym:
                    note = "format attendu: année (AAAA) ou intervale (AAAA/AAAA)"
                    yield YearIntervalValueError.from_row(
                        row, note=note, field_name=self.column
                    )

                # Year ok
                return

            # not a period -> add error
            note = "format attendu: AAAA/AAAA"
            yield YearIntervalValueError.from_row(
                row, note=note, field_name=self.column
            )
            return

        year1 = int(rm.group(1))
        year2 = int(rm.group(2))
        if year1 == year2:
            note = "les deux années doivent être différentes"
            yield YearIntervalValueError.from_row(
                row, note=note, field_name=self.column
            )
            return

        if year1 > year2:
            note = (
                f"la deuxième année ({year1}) doit être postérieure"
                " à la première ({year2})"
            )
            yield YearIntervalValueError.from_row(
                row, note=note, field_name=self.column
            )
            return

    @classmethod
    def metadata_select_class(cls, type: Optional[str]) -> Type[Self]:
        return cls

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column"],
        "properties": {
            "column": {"type": "string"},
            "allow-year-only": {"type": "string"},
        },
    }
