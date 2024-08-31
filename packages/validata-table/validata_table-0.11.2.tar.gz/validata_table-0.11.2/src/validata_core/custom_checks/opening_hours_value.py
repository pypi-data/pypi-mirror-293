import opening_hours

from validata_core.domain.types import ValidationResult

from .format_check import FormatCheck


def opening_hours_validator(value: str, **options) -> ValidationResult:
    if not opening_hours.validate(value):  # type: ignore
        return False, ""
    return True, ""


template = (
    "La valeur '{cell}' n'est pas une définition d'horaire d'ouverture correcte.\n\n"
    " Celle-ci doit respecter la spécification"
    " [OpenStreetMap](https://wiki.openstreetmap.org/wiki/Key:opening_hours)"
    " de description d'horaires d'ouverture."
)

OpeningHoursValue = FormatCheck(
    opening_hours_validator,
    "opening-hours-value",
    "Horaires d'ouverture incorrects",
    "",
    template,
)
