"""
    Comme indiqué par Loïc Haÿ dans son mail du 5/7/2018

> Document de référence dans les spécifications SCDL :
> http://www.moselle.gouv.fr/content/download/1107/7994/file/nomenclature.pdf
>
> Dans la nomenclature Actes, les valeurs avant le "/" sont :
>
> Commande publique
> Urbanisme
> Domaine et patrimoine
> Fonction publique
> Institutions et vie politique
> Libertés publiques et pouvoirs de police
> Finances locales
> Domaines de compétences par thèmes
> Autres domaines de compétences
>
> Le custom check devra accepter minuscules et majuscules, accents et sans accents ...

    Pierre Dittgen, JailBreak
"""
import unicodedata

from validata_core.domain.types import ValidationResult

from .format_check import FormatCheck


def norm_str(s):
    """Normalize string, i.e. removing accents and turning into lowercases"""
    return "".join(
        c
        for c in unicodedata.normalize("NFD", s.lower())
        if unicodedata.category(c) != "Mn"
    )


NORMALIZED_AUTHORIZED_VALUES = set(
    map(
        norm_str,
        [
            "Commande publique",
            "Urbanisme",
            "Domaine et patrimoine",
            "Fonction publique",
            "Institutions et vie politique",
            "Libertés publiques et pouvoirs de police",
            "Finances locales",
            "Domaines de compétences par thèmes",
            "Autres domaines de compétences",
        ],
    )
)


def nomenclature_actes_validator(value, **options) -> ValidationResult:
    if "/" not in value:
        return False, "le signe oblique « / » est manquant"

    nomenc = value[: value.find("/")]

    # Nomenclature reconnue et pas d'espace avant ni après l'oblique
    if norm_str(nomenc) in NORMALIZED_AUTHORIZED_VALUES and "/ " not in value:
        return True, ""

    if norm_str(nomenc.rstrip()) in NORMALIZED_AUTHORIZED_VALUES or "/ " in value:
        return False, "Le signe oblique ne doit pas être précédé ni suivi d'espace"
    else:
        return False, f"le préfixe de nomenclature Actes {nomenc!r} n'est pas reconnu"


NomenclatureActesValue = FormatCheck(
    nomenclature_actes_validator,
    "nomenclature-actes-value",
    "Actes de nomenclature",
    "",
    (
        "La valeur {cell!r} ne respecte pas le format des nomenclatures d'actes"
        " ({note})"
    ),
)
