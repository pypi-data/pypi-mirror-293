import stdnum.fr.siren

from validata_core.domain.types import ValidationResult

from .format_check import FormatCheck


def siren_validator(value: str, **kwargs) -> ValidationResult:
    if not stdnum.fr.siren.is_valid(value):
        return False, ""
    return True, ""


FrenchSirenValue = FormatCheck(
    siren_validator,
    "french-siren-value",
    "Numéro SIREN invalide",
    (
        "Le numéro de SIREN indiqué n'est pas valide selon la définition"
        " de l'[INSEE](https://www.insee.fr/fr/metadonnees/definition/c2047)."
    ),
    "La valeur {cell} n'est pas un numéro SIREN français valide.",
)
