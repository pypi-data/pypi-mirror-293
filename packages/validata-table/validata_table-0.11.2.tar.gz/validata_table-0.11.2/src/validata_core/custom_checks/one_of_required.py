# -*- coding: utf-8 -*-
"""
    One of required check

    Ce custom check vérifie :
    - Pour les deux colonnes relatives à ce custom check, pour une ligne donnée, au moins une des deux colonnes doit
    contenir une valeur,
    - Pour une ligne donnée, les deux colonnes peuvent contenir chacune une valeur,
    - Si une des deux colonnes est manquantes, alors toute valeur manquante dans l'autre colonne engendre une erreur de
    validation,
    - Si les deux colonnes sont manquantes cela engendre une erreur de validation.


    Paramètres :
    - column1 : la première colonne
    - column2 : la deuxième colonne

    Messages d'erreur attendus :
    - Les colonnes {nom de la première colonne} et {nom de la deuxième colonne} sont manquantes.
    - Au moins l'une des colonnes {liste des noms de colonnes} doit comporter une valeur.

    Amélie Rondot, multi
"""
from typing import Iterable, List, Optional, Type, Union

import attrs
import frictionless
from frictionless import Row, errors, resources, types
from typing_extensions import Self

from .utils import CustomCheckMultipleColumns, valued

# Module API


class OneOfRequiredRowError(errors.RowError):
    """Custom error."""

    type = "one-of-required"
    name = "Une des deux colonnes requises"
    title = name
    tags = ["#body"]
    template = "incohérence relevée ({note})."
    description = ""


class OneOfRequiredTableError(errors.TableError):
    """Custom error."""

    type = "one-of-required"
    name = "Une des deux colonnes requises"
    title = name
    tags = ["#head", "#structure"]
    template = "Une des deux colonnes requises : {note}"
    description = ""


OneOfRequiredError = Union[OneOfRequiredRowError, OneOfRequiredTableError]


@attrs.define(kw_only=True, repr=False)
class OneOfRequired(CustomCheckMultipleColumns):
    """
    One of required check class
    """

    type = "one-of-required"
    column1: str = ""
    id: str = ""

    Errors = [OneOfRequiredRowError]

    @classmethod
    def from_descriptor(cls, descriptor: Union[str, types.IDescriptor]) -> Self:
        if isinstance(descriptor, dict) and "id" in descriptor.keys():
            cls.id = descriptor["id"]
        else:
            cls.id = ""
        if isinstance(descriptor, dict) and "column1" in descriptor.keys():
            cls.column1 = descriptor["column1"]
        else:
            cls.column1 = ""
        return super().from_descriptor(descriptor)

    def validate_start(
        self,
    ) -> Iterable[errors.Error]:
        assert isinstance(self.resource, resources.table.TableResource)
        if self.resource.sample == []:
            note = "Les données source ne peuvent pas être vides."
            yield OneOfRequiredTableError(note=note)
        elif (
            self.column1 not in self.resource.header
            and self.column2 not in self.resource.header
        ):
            note = f"Les deux colonnes {self.column1!r} et {self.column2!r} sont manquantes."
            yield OneOfRequiredTableError(note=note)

    def validate_row(self, row: Row) -> Iterable[errors.Error]:
        assert isinstance(self.resource, resources.table.TableResource)
        if self.resource.sample == []:
            # empty data file
            # one-of-required error has already been generated in validate_start()
            return []

        elif (
            self.column1 not in self.resource.header
            and self.column2 not in self.resource.header
        ):
            # one-of-required error has already been generated in validate_start()
            return []
        else:
            cell_value1 = row[self.column1]
            cell_value2 = row[self.column2]

            if not valued(cell_value1) and not valued(cell_value2):
                note = (
                    f"Au moins l'une des colonnes {self.column1!r} ou {self.column2!r} "
                    "doit comporter une valeur."
                )
                yield OneOfRequiredRowError.from_row(
                    row,
                    note=note,
                )

    def _validate_start(self, all_columns: List[str]) -> Iterable[errors.Error]:
        return []

    def _validate_row(self, row: frictionless.Row) -> Iterable[errors.Error]:
        return []

    @classmethod
    def metadata_select_class(cls, type: Optional[str]) -> Type[Self]:
        return cls

    metadata_profile = {  # type: ignore
        "type": "object",
        "required": ["column1", "column2"],
        "properties": {"column1": {"type": "string"}, "column2": {"type": "string"}},
    }
