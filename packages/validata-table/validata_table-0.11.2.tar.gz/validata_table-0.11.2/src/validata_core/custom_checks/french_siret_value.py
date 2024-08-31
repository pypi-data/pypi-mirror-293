import stdnum.fr.siret

from validata_core.domain.types import ValidationResult

from .format_check import FormatCheck


def siret_validator(value: str, **options) -> ValidationResult:
    if not stdnum.fr.siret.is_valid(value):
        return False, ""
    return True, ""


FrenchSiretValue = FormatCheck(
    siret_validator,
    "french-siret-value",
    "Numéro SIRET invalide",
    (
        "Le numéro de SIRET indiqué n'est pas valide selon la définition"
        " de l'[INSEE](https://www.insee.fr/fr/metadonnees/definition/c1841)."
    ),
    "La valeur {cell} n'est pas un numéro SIRET français valide.",
)
