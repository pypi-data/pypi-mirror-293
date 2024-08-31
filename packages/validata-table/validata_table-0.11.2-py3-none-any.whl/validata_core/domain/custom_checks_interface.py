from typing import Any, Dict, List, Optional, Tuple

import frictionless
from frictionless import Check

from validata_core.custom_checks import available_checks
from validata_core.custom_checks.format_check import FormatCheck
from validata_core.custom_checks.utils import build_check_error
from validata_core.domain.spi import CustomFormatsRepository
from validata_core.domain.types import CustomCheck, Error, FrFormat, Schema

VALIDATA_MAX_ROWS = 100000


def build_custom_checks(
    schema: Schema, custom_formats_repository: CustomFormatsRepository
) -> Tuple[List[Check], List[Error]]:
    """Build custom checks.

    If a custom check is not valid, a CheckError is returned.

    Returned custom-checks are :

    - a maximum row number check that always applies
    - checks defined in the top-level "custom_checks" property
    - fields property "frFormat"
    """

    # limit amount of rows to read
    validation_checks = [_max_rows_check(VALIDATA_MAX_ROWS)]

    custom_checks, check_errors = _from_custom_checks_prop(schema)
    validation_checks += custom_checks

    fr_format_checks, fr_format_errors = _from_frformat_props(
        schema, custom_formats_repository
    )
    validation_checks += fr_format_checks
    check_errors += fr_format_errors

    return validation_checks, check_errors


def _max_rows_check(max_rows) -> Check:
    return frictionless.Check.from_descriptor(
        {"type": "table-dimensions", "maxRows": max_rows}
    )


def _from_custom_checks_prop(schema: Schema) -> Tuple[List[Check], List[Error]]:
    custom_checks = schema.get_custom_checks()

    # Dynamically add custom check based on schema needs
    check_errors: List[Error] = []
    validation_checks = []

    for custom_check in custom_checks:
        check, error = _single_custom_check_prop(custom_check)

        if error:
            check_errors.append(error)

        if check:
            validation_checks.append(check)
    return validation_checks, check_errors


def _single_custom_check_prop(
    custom_check: CustomCheck,
) -> Tuple[Optional[Check], Optional[Error]]:
    check_name = custom_check.name

    if check_name not in available_checks:
        return None, Error(
            build_check_error(
                check_name,
                note=f"Tentative de définir le custom check {check_name}, qui n'est pas connu.",
            )
        )
    check_class = available_checks[check_name]
    check_params = custom_check.params

    return check_class.from_descriptor(descriptor=check_params), None


def _from_frformat_props(
    schema: Schema, custom_formats_repository: CustomFormatsRepository
) -> Tuple[List[Check], List[Error]]:
    frformat_checks: List[Check] = []
    frformat_errors: List[Error] = []

    for field in schema.get_fields():
        if field.fr_format:
            check, error = _single_frformat_prop(
                field.fr_format, field.name, custom_formats_repository
            )

            if error:
                frformat_errors.append(error)

            if check:
                frformat_checks.append(check)

    return frformat_checks, frformat_errors


def _single_frformat_prop(
    frformat: FrFormat,
    fieldname: str,
    custom_formats_repository: CustomFormatsRepository,
) -> Tuple[Optional[Check], Optional[Error]]:
    frformat_options: Dict[str, Any] = {}

    if not isinstance(frformat, str):
        frformat_code = frformat.name
        frformat_options = frformat.options
    else:
        frformat_code = frformat

    if frformat_code not in custom_formats_repository.ls():
        return None, Error(
            build_check_error(
                str(frformat_code),
                note='valeur de la propriété "frFormat" inconnue.',
            )
        )

    validate = custom_formats_repository.get_validator(frformat_code)
    description = custom_formats_repository.get_description(frformat_code)

    frformat_title = frformat_code.replace("-", " ").title()
    format_check = FormatCheck(
        validate,
        f"{frformat_code}-fr-format",
        f"{frformat_title} invalide",
        description,
        f"La valeur n'est pas conforme au format {frformat_title}." " {note}",
        available_options=list(frformat_options.keys()),
    )

    return (
        format_check.to_frictionless_check(fieldname, **frformat_options),
        None,
    )
