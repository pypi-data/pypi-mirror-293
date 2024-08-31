import phonenumbers

from validata_core.domain.types import ValidationResult

from .format_check import FormatCheck


def phone_number_validator(value: str, **options) -> ValidationResult:
    """Check if a phone number is a french or international valid one."""
    return (
        is_valid_number_for_country(value, country_code="FR")
        or is_valid_number_for_country(value),
        "",
    )


def is_valid_number_for_country(phone_number: str, *, country_code=None):
    """Check if a phone number, giving an optional country_code.

    If country code is given, an additional check for valid_short_number is done.
    """
    try:
        pn = phonenumbers.parse(phone_number, country_code)
    except phonenumbers.NumberParseException:
        return False

    std_valid = phonenumbers.is_valid_number(pn)
    return (
        std_valid
        if country_code is None
        else std_valid or phonenumbers.is_valid_short_number(pn)
    )


template = (
    "La valeur '{cell}' n'est pas un numéro de téléphone valide.\n\n"
    " Les numéros de téléphone acceptés sont les numéros français à 10 chiffres"
    " (`01 99 00 27 37`) ou au format international avec le préfixe du pays"
    " (`+33 1 99 00 27 37`). Les numéros courts (`115` ou `3949`) sont"
    " également acceptés."
)

PhoneNumberValue = FormatCheck(
    phone_number_validator,
    "phone-number-value",
    "Numéro de téléphone invalide",
    "",
    template,
)
