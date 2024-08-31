import re
from datetime import datetime
from typing import Any, List, Optional, Protocol, Type

import frictionless
import frictionless.errors as ferr
import frictionless.fields as frfields
from typing_extensions import TypeGuard, TypeVar

from validata_core.domain.types import ConstraintError, Error, ErrTxt, Schema

DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")


class Locale(Protocol):
    """Locale is an interface for defining custom error strings"""

    def required(self) -> ErrTxt:
        """Returns error info for "required" schema validation"""
        ...

    def unique(self) -> ErrTxt:
        """Returns error info for "unique" schema validation"""
        ...

    def min_length(self, cell_value: Any, min: Any) -> ErrTxt:
        """Returns error info for "minLength" schema validation"""
        ...

    def max_length(self, cell_value: Any, max: Any) -> ErrTxt:
        """Returns error info for "maxLength" schema validation"""
        ...

    def minimum(self, cell_value: Any, min: Any) -> ErrTxt:
        """Returns error info for "minimum" schema validation"""
        ...

    def maximum(self, cell_value: Any, max: Any) -> ErrTxt:
        """Returns error info for "maximum" schema validation"""
        ...

    def pattern(
        self, cell_value: Any, pattern: Any, context: Optional[frictionless.Field]
    ) -> ErrTxt:
        """Returns error info for "pattern" schema validation"""
        ...

    def enum(self, enum_values: Any) -> ErrTxt:
        """Returns error info for "enum" schema validation"""
        ...


class FrLocale(Locale):
    def required(self) -> ErrTxt:
        return "Cellule vide", "Une valeur doit être renseignée."

    def unique(self) -> ErrTxt:
        return (
            "Valeur déjà présente",
            "Toutes les valeurs de cette colonne doivent être uniques.",
        )

    def min_length(self, cell_value: Any, min: Any) -> ErrTxt:
        msg = (
            f"Le texte attendu doit comporter au moins {min} caractère(s)"
            f" (au lieu de {len(cell_value)} actuellement)."
        )
        return "Valeur trop courte", msg

    def max_length(self, cell_value: Any, max: Any) -> ErrTxt:
        msg = (
            f"Le texte attendu ne doit pas comporter plus de {max}"
            f" caractère(s) (au lieu de {len(cell_value)} actuellement)."
        )
        return "Valeur trop longue", msg

    def minimum(self, cell_value: Any, min: Any) -> ErrTxt:
        return (
            "Valeur trop petite",
            f"La valeur attendue doit être au moins égale à {min}.",
        )

    def maximum(self, cell_value: Any, max: Any) -> ErrTxt:
        return (
            "Valeur trop grande",
            f"La valeur attendue doit être au plus égale à {max}.",
        )

    def pattern(
        self,
        cell_value: Any,
        pattern: Any,
        context: Optional[frictionless.Field],
    ) -> ErrTxt:
        info_list = [
            f"{cell_value} ne respecte pas le motif imposé (expression régulière : {pattern})\n"
        ]
        if context and context.description:
            info_list.append(context.description + "\n")
        if context and context.example:
            info_list.append(f"## Exemple(s) valide(s)\n{context.example}\n")
        msg = (
            "\n".join(info_list)
            if info_list
            else "*Aucune description ni exemple à afficher.*"
        )
        return "Format incorrect", msg

    def enum(self, enum_values: Any) -> ErrTxt:
        if len(enum_values) == 1:
            return (
                "Valeur incorrecte",
                f"L'unique valeur autorisée est : {enum_values[0]}.",
            )

        else:
            md_str = "\n".join([f"- {val}" for val in enum_values])
            return (
                "Valeur incorrecte",
                f"Les seules valeurs autorisées sont :\n{md_str}",
            )


def translate_errors(
    errors: List[Error], schema: Schema, locale: Locale
) -> List[Error]:
    return [translate_one_error(err, locale, schema) for err in errors]


def translate_one_error(
    err: Error, locale: Locale, schema: Optional[Schema] = None
) -> Error:
    """Translate and improve error message clarity.

    Update err fields:
    - title: use a french human readable name describing the error type
    - message: french error message

    And return updated error
    """

    error_translation = translate_title_and_message(err, locale, schema)

    err.set_translation(error_translation)

    if error_translation != ("", ""):
        err.title = error_translation[0]
        err.message = error_translation[1]
        return err
    else:
        return err


def translate_title_and_message(
    err: Error, locale: Locale, schema: Optional[Schema]
) -> ErrTxt:
    frless_err = err.frless_error

    if _is_error_class(frless_err, ferr.EncodingError):
        return encoding_error(frless_err)

    elif _is_error_class(frless_err, ferr.BlankHeaderError):
        return blank_header_error(frless_err)

    elif _is_error_class(frless_err, ferr.BlankRowError):
        return blank_row_error()

    elif _is_error_class(frless_err, ferr.ExtraCellError):
        return extra_cell_error()

    elif _is_error_class(frless_err, ferr.TypeError):
        return type_error(frless_err, schema)

    elif _is_error_class(frless_err, ferr.ConstraintError):
        return constraint_error(frless_err, schema, locale)

    elif _is_error_class(frless_err, ferr.MissingLabelError):
        return missing_label_error(frless_err)

    elif (
        _is_error_class(frless_err, ferr.Error)
        and err.message == '"schema_sync" requires unique labels in the header'
    ):
        return schema_sync_error()

    return ("", "")


def et_join(values: List[str]) -> str:
    """french enum
    >>> et_join([])
    ''
    >>> et_join(['a'])
    'a'
    >>> et_join(['a','b'])
    'a et b'
    >>> et_join(['a','b','c'])
    'a, b et c'
    >>> et_join(['a','b','c','d','e'])
    'a, b, c, d et e'
    """
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    return " et ".join([", ".join(values[:-1]), values[-1]])


def encoding_error(err: ferr.Error) -> ErrTxt:
    """Return french name and french message related to
    'encoding' frictionless error.
    """
    return (
        "Erreur d'encodage",
        f"Un problème d'encodage empêche la lecture du fichier ({err.note})",
    )


def blank_header_error(err: ferr.BlankHeaderError) -> ErrTxt:
    """Return french name and french message related to
    'blanck header' frictionless error.
    """
    title = "En-tête manquant"
    if len(err.row_numbers) == 1:
        message = f"La colonne n°{err.row_numbers[0]} n'a pas d'entête."
    else:
        pos_list = ", ".join(str(err.row_numbers))
        message = f"Les colonnes n°{pos_list} n'ont pas d'entête."
    return (title, message)


def blank_row_error() -> ErrTxt:
    """Return french name and french message related to
    'blanck row' frictionless error.
    """
    return ("Ligne vide", "Les lignes vides doivent être retirées de la table.")


def extra_cell_error() -> ErrTxt:
    """Return french name and french message related to
    'extra cell' frictionless error.
    """
    return (
        "Valeur surnuméraire",
        "Le nombre de cellules de cette ligne excède le nombre de colonnes défini dans le schéma.",
    )


def date_type_error(field_value: Any) -> ErrTxt:
    title = "Format de date incorrect"

    if _is_french_date_format(field_value):
        isodate = _convert_french_to_iso_date(field_value)
        message = f"La forme attendue est {isodate}."
        return (title, message)

    # Checks if date is yyyy-mm-ddThh:MM:ss
    # print('DATE TIME ? [{}]'.format(field_value))
    dm = DATETIME_RE.match(field_value)
    if dm:
        iso_date = field_value[: field_value.find("T")]
        message = f"La forme attendue est {iso_date!r}."
        return (title, message)

    # default
    message = "La date doit être écrite sous la forme `aaaa-mm-jj`."

    return (title, message)


def number_type_error(field_value: Any) -> ErrTxt:
    title = "Format de nombre incorrect"
    if "," in field_value:
        en_number = field_value.replace(",", ".")
        value_str = f"«&#160;{en_number}&#160;»"
        message = f"Le séparateur décimal à utiliser est le point ({value_str})."
    else:
        message = (
            "La valeur ne doit comporter que des chiffres"
            " et le point comme séparateur décimal."
        )
    return (title, message)


def string_type_error(field_format: Any) -> ErrTxt:
    title = "Format de chaîne incorrect"
    if field_format == "uri":
        message = "La valeur doit être une adresse de site ou de page internet (URL)."
    elif field_format == "email":
        message = "La valeur doit être une adresse email."
    elif field_format == "binary":
        message = "La valeur doit être une chaîne encodée en base64."
    elif field_format == "uuid":
        message = "La valeur doit être un UUID."
    else:
        message = "La valeur doit être une chaîne de caractères."

    return (title, message)


def boolean_type_error(field_def: frfields.boolean.BooleanField) -> ErrTxt:
    true_values = field_def.true_values if field_def.true_values else ["true"]
    false_values = field_def.false_values if field_def.false_values else ["false"]
    true_values_str = et_join(list(map(lambda v: "`{}`".format(v), true_values)))
    false_values_str = et_join(list(map(lambda v: "`{}`".format(v), false_values)))
    title = "Valeur booléenne incorrecte"
    message = (
        f"Les valeurs acceptées sont {true_values_str} (vrai)"
        f" et {false_values_str} (faux)."
    )

    return (title, message)


def type_error(err: ferr.TypeError, schema: Optional[Schema]) -> ErrTxt:
    """Return french name and french message related to
    'type' frictionless error.
    """
    field_name = err.field_name
    field_def = schema.find_field_in_schema(field_name) if schema else None

    if field_def is None:
        return ("", "")

    field_format = field_def.format
    field_value = err.cell

    if isinstance(field_def, frfields.date.DateField):
        return date_type_error(field_value)

    elif isinstance(field_def, frfields.year.YearField):
        title = "Format d'année incorrect"
        message = "L'année doit être composée de 4 chiffres."

    elif isinstance(field_def, frfields.number.NumberField):
        return number_type_error(field_value)

    elif isinstance(field_def, frfields.integer.IntegerField):
        title = "Format entier incorrect"
        message = "La valeur doit être un nombre entier."

    elif isinstance(field_def, frfields.string.StringField):
        return string_type_error(field_format)

    elif isinstance(field_def, frfields.boolean.BooleanField):
        return boolean_type_error(field_def)

    else:
        title, message = ("Cette erreur ne devrait jamais arriver", "")

    return (title, message)


def constraint_error(
    err: ferr.ConstraintError, schema: Optional[Schema], locale: Locale
) -> ErrTxt:
    """Return french name and french message related to
    'constraint' frictionless error.
    """

    err_with_context = ConstraintError(err, schema)
    c = err_with_context.violated_constraint
    cell = err_with_context.cell_value
    constraint_val = err_with_context.get_constraint_value()
    field_def = err_with_context.field_def

    if c == "required":
        return locale.required()

    if c == "unique":
        return locale.unique()

    if c == "minLength":
        return locale.min_length(cell, constraint_val)

    if c == "maxLength":
        return locale.max_length(cell, constraint_val)

    if c == "minimun":
        return locale.minimum(cell, constraint_val)

    if c == "maximum":
        return locale.maximum(cell, constraint_val)

    if c == "pattern":
        return locale.pattern(cell, constraint_val, field_def)

    if c == "enum":
        return locale.enum(constraint_val)

    else:
        return _unknown_constraint_error(err)


def missing_label_error(err: ferr.MissingLabelError) -> ErrTxt:
    """Return french name and french message related to
    'missing-label' frictionless error.
    """
    field_name = err.field_name
    return (
        "Colonne obligatoire manquante",
        f"La colonne obligatoire `{field_name}` est manquante.",
    )


def schema_sync_error() -> ErrTxt:
    title = "Colonnes dupliquées"
    message = "Le fichier  comporte des colonnes avec le même nom. Pour valider le fichier, veuillez d'abord le corriger en mettant des \
                valeurs uniques dans son en-tête (la première ligne du fichier)."
    return (title, message)


C = TypeVar("C", bound=ferr.Error)


def _is_error_class(err: ferr.Error, error_class: Type[C]) -> TypeGuard[C]:
    return err.type == error_class.type and isinstance(err, error_class)


def _is_french_date_format(date_string: str) -> bool:
    try:
        datetime.strptime(date_string, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def _convert_french_to_iso_date(date_string: str) -> str:
    """Expects date_string to be validated as a valid french date"""
    return datetime.strptime(date_string, "%d/%m/%Y").strftime("%Y-%m-%d")


def _unknown_constraint_error(err: ferr.Error) -> ErrTxt:
    return ("Contrainte non repectée", err.note)
