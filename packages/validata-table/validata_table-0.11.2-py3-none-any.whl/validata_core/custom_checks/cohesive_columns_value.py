# -*- coding: utf-8 -*-
"""
    Cohesive columns value check

    Vérifie que pour une liste de colonnes donnée, toutes les colonnes ont une valeur
    ou aucune des colonnes n'a une valeur

    Paramètres :
    - column : la première colonne
    - othercolumns : les autres colonnes qui doivent être remplies (ou non)

    Messages d'erreur attendus :
    - Colonne(s) non trouvée(s) : {liste de noms de colonnes non trouvées}
    - Les colonnes {liste des noms de colonnes} doivent toutes comporter une valeur
    ou toutes être vides

    Pierre Dittgen, Jailbreak
"""
from typing import Iterable, Optional, Type, Union

import attrs
import frictionless
from frictionless import errors, types
from typing_extensions import Self

from validata_core.custom_checks.utils import (
    CustomCheckMultipleColumns,
    build_check_error,
)

# Module API


class CohesiveColumnsValueError(errors.CellError):
    """Custom error."""

    type = "cohesive-columns-value"
    name = "Cohérence entre colonnes"
    title = name
    tags = ["#body"]
    template = "incohérence relevée ({note})."
    description = ""


@attrs.define(kw_only=True, repr=False)
class CohesiveColumnsValue(CustomCheckMultipleColumns):
    """
    Cohesive columns value check class
    """

    type = "cohesive-columns-value"
    columns_nb: int = 1
    skip_empty_cells: bool = False

    Errors = [CohesiveColumnsValueError]

    @classmethod
    def from_descriptor(cls, descriptor: Union[str, types.IDescriptor]) -> Self:
        if isinstance(descriptor, dict):
            if "column" in descriptor.keys() and "othercolumns" in descriptor.keys():
                all_columns = [descriptor["column"]] + descriptor["othercolumns"]
            elif "column" in descriptor.keys():
                all_columns = [descriptor["column"]]
            elif "othercolumns" in descriptor.keys():
                all_columns = descriptor["othercolumns"]
            else:
                all_columns = []
        else:
            all_columns = []
        cls.columns_nb = len(all_columns)
        cls.skip_empty_cells = False
        return super().from_descriptor(descriptor=descriptor)

    def _validate_start(self, all_columns: list[str]) -> Iterable[errors.Error]:
        if not self.resource.data:
            note = "Les données sources ne peuvent pas être vides."
            yield build_check_error(CohesiveColumnsValue.type, note)
        elif self.column not in self.resource.data[0]:
            note = f"La colonne {self.column!r} est manquante."
            yield build_check_error(CohesiveColumnsValue.type, note)
        elif not self.othercolumns or len(self.othercolumns) == 0:
            note = "La liste de colonnes à comparer est vide"
            yield build_check_error(CohesiveColumnsValue.type, note)
        else:
            for col in self.othercolumns:
                if col not in self.resource.schema.field_names:
                    note = f"La colonne à comparer {col!r} est manquante"
                    yield build_check_error(CohesiveColumnsValue.type, note)

    def validate_row(self, row: frictionless.Row) -> Iterable[errors.Error]:
        cell_value = row[self.column]

        status = valued(cell_value)
        if self.othercolumns:
            other_cell_values = [row[col] for col in self.othercolumns]
        else:
            other_cell_values = []

        # test if all columns are valued or all columns are empty
        if any(valued(v) != status for v in other_cell_values):
            columns_str = ", ".join(self.get_all_columns())
            note = (
                f"Les colonnes {columns_str} doivent toutes comporter une valeur"
                " ou toutes être vides"
            )
            yield CohesiveColumnsValueError.from_row(
                row, note=note, field_name=self.column
            )

    def _validate_row(self, row: frictionless.Row) -> Iterable[errors.Error]:
        return []

    @classmethod
    def metadata_select_class(cls, type: Optional[str]) -> Type[Self]:
        return cls

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column", "othercolumns"],
        "properties": {"column": {"type": "string"}, "othercolumns": {"type": "array"}},
    }


def valued(val):
    return val is not None and val != ""
