"""Routes."""

import copy
import io
import json
import logging
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, Iterable, List, Optional, Set, Tuple, Union
from urllib.parse import urlencode
from urllib.request import urlopen

import frictionless
import requests
from commonmark import commonmark
from flask import Request, abort, redirect, render_template, request, url_for
from flask_babel import _
from jsonschema import exceptions
from opendataschema import GitSchemaReference, SchemaCatalog, by_commit_date
from werkzeug.wrappers.response import Response

from validata_core import resource_service as resource
from validata_core import validation_service
from validata_core.domain.helpers import is_body_error, is_structure_error, to_lower
from validata_core.domain.types import Error, Header, Report, Row, ValidataResource
from validata_ui.app import app, config, fetch_schema, schema_catalog_registry
from validata_ui.app.model import Section
from validata_ui.app.ui_util import ThreadUpdater, flash_error, flash_warning
from validata_ui.app.validata_util import strip_accents

log = logging.getLogger(__name__)

schema_catalog_updater: Dict[str, ThreadUpdater] = {}


def get_schema_catalog(section_name: str) -> SchemaCatalog:
    """Return a schema catalog associated to a section_name."""
    global schema_catalog_updater

    if section_name not in schema_catalog_updater:
        schema_catalog_updater[section_name] = ThreadUpdater(
            lambda: schema_catalog_registry.build_schema_catalog(section_name)
        )
    return schema_catalog_updater[section_name].value


class SchemaInstance:
    """Handy class to handle schema information."""

    def __init__(self, parameter_dict: Dict[str, Any]):
        """Initialize schema instance and tableschema catalog."""

        self.section_name = None
        self.section_title = None
        self.name = None
        self.url = None
        self.ref = None
        self.reference = None
        self.doc_url = None
        self.branches = None
        self.tags = None

        # From schema_url
        if parameter_dict.get("schema_url"):
            self.url = parameter_dict["schema_url"]
            self.section_title = _("Autre schéma")

        # from schema_name (and schema_ref)
        elif parameter_dict.get("schema_name"):
            self.schema_and_section_name = parameter_dict["schema_name"]
            self.ref = parameter_dict.get("schema_ref")

            # Check schema name
            chunks = self.schema_and_section_name.split(".")
            if len(chunks) != 2:
                abort(400, _("Paramètre 'schema_name' invalide"))

            self.section_name, self.name = chunks
            self.section_title = self.find_section_title(self.section_name)

            # Look for schema catalog first
            try:
                table_schema_catalog = get_schema_catalog(self.section_name)
            except Exception:
                log.exception("")
                abort(400, _("Erreur de traitement du catalogue"))
            if table_schema_catalog is None:
                abort(400, _("Catalogue indisponible"))

            schema_reference = table_schema_catalog.reference_by_name.get(self.name)
            if schema_reference is None:
                abort(
                    400,
                    f"Schéma {self.name!r} non trouvé dans le catalogue de la "
                    f"section {self.section_name!r}",
                )

            if isinstance(schema_reference, GitSchemaReference):
                self.tags = sorted(
                    schema_reference.iter_tags(), key=by_commit_date, reverse=True
                )
                if self.ref is None:
                    schema_ref = (
                        self.tags[0]
                        if self.tags
                        else schema_reference.get_default_branch()
                    )
                    abort(
                        redirect(
                            compute_validation_form_url(
                                {
                                    "schema_name": self.schema_and_section_name,
                                    "schema_ref": schema_ref.name,
                                }
                            )
                        )
                    )
                tag_names = [tag.name for tag in self.tags]
                self.branches = [
                    branch
                    for branch in schema_reference.iter_branches()
                    if branch.name not in tag_names
                ]
                self.doc_url = schema_reference.get_doc_url(
                    ref=self.ref
                ) or schema_reference.get_project_url(ref=self.ref)

            self.url = schema_reference.get_schema_url(ref=self.ref)

        else:
            flash_error(_("Erreur dans la récupération des informations de schéma"))
            abort(redirect(url_for("home")))

        try:
            self.schema = fetch_schema(self.url)
        except json.JSONDecodeError as e:
            err_msg = (
                _("Le schéma fourni n'est pas un fichier JSON valide") + f" : { e }"
            )
            log.exception(err_msg)
            flash_error(err_msg)
            abort(redirect(url_for("home")))
        except Exception as e:
            err_msg = (
                _("Une erreur est survenue en récupérant le schéma)") + f" : { e }"
            )
            log.exception(err_msg)
            flash_error(err_msg)
            abort(redirect(url_for("home")))

    def request_parameters(self) -> Dict[str, Any]:
        """Build request parameter dict to identify schema."""
        return (
            {
                "schema_name": self.schema_and_section_name,
                "schema_ref": "" if self.ref is None else self.ref,
            }
            if self.name
            else {"schema_url": self.url}
        )

    def find_section_title(self, section_name: str) -> Optional[str]:
        """Return section title or None if not found."""
        if config.CONFIG:
            for section in config.CONFIG.homepage.sections:
                if section.name == section_name:
                    return section.title
        return None


def build_template_source_data(
    header: Header, rows: List[Row], preview_rows_nb: int = 5
) -> Dict[str, Any]:
    """Build source data information to preview in validation report page."""
    source_header_info = [(colname, False) for colname in header]

    rows_count = len(rows)
    preview_rows_count = min(preview_rows_nb, rows_count)
    return {
        "source_header_info": source_header_info,
        "header": header,
        "rows_nb": rows_count,
        "data_rows": rows,
        "preview_rows_count": preview_rows_count,
        "preview_rows": rows[:preview_rows_count],
    }


def build_ui_errors(errors: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Add context to errors, converts markdown content to HTML."""

    def improve_err(err: Dict[str, Any]) -> Dict[str, Any]:
        """Add context info based on row-nb presence and converts content to HTML."""
        # Context
        update_keys = {
            "context": (
                "body"
                if "row-number" in err and err["row-number"] is not None
                else "table"
            ),
        }

        # Set title
        if "title" not in err:
            update_keys["title"] = err["name"]

        # Set content
        content = "*content soon available*"
        if "message" in err:
            content = err["message"]
        elif "description" in err:
            content = err["description"]
        update_keys["content"] = commonmark(content)

        return {**err, **update_keys}

    return list(map(improve_err, errors))


def add_source_headers_and_source_dimensions(
    ui_report: Dict[str, Any],
    headers: List[str],
    rows_count: int,
):
    """Add source headrs and source dimensions to the UI report"""
    # source headers
    ui_report["table"]["header"] = headers

    # source dimension
    ui_report["table"]["col_count"] = len(headers)
    ui_report["table"]["row_count"] = rows_count


def get_headers_and_fields_dict_among_case_sensitivity(
    header_case: bool,
    headers: List[str],
    fields_dict: Dict[Any, tuple[Any, Any]],
) -> Tuple[List[str], Dict[Any, tuple[Any, Any]]]:
    """Returns a tuple including :
    - the list of headers, converted in lower case if case-insensitive,
    - the schema fields in dictionnary form, with name fields converted
    in lower case if case-insensitive.
    """

    if header_case:
        return (
            headers,
            fields_dict,
        )
    else:
        return (
            to_lower(headers),
            {field.lower(): fields_dict[field] for field in fields_dict.keys()},
        )


def add_header_titles_and_description(
    ui_report: Dict[str, Any],
    fields_dict: Dict[Any, tuple[Any, Any]],
    header_case: bool,
    headers: List[str],
):
    """Add headers' titles and headers' description to
    the UI report
    """
    (
        converted_headers,
        converted_fields_dict,
    ) = get_headers_and_fields_dict_among_case_sensitivity(
        header_case, headers, fields_dict
    )

    ui_report["table"]["headers_title"] = [
        (
            converted_fields_dict[h][0]
            if h in converted_fields_dict
            else _("Colonne inconnue")
        )
        for h in converted_headers
    ]

    ui_report["table"]["headers_description"] = [
        (
            converted_fields_dict[h][1]
            if h in converted_fields_dict
            else _("Cette colonne n'est pas définie dans le schema")
        )
        for h in converted_headers
    ]


def add_columns_alerts(
    table_report: Dict[str, Any],
    ui_report: Dict[str, Any],
    fields_dict: Dict[Any, tuple[Any, Any]],
    headers: List[str],
    header_case: bool,
):
    """Add columns alerts to the UI report"""
    (
        converted_headers,
        converted_fields_dict,
    ) = get_headers_and_fields_dict_among_case_sensitivity(
        header_case, headers, fields_dict
    )

    missing_headers = [
        err["fieldName"]
        for err in table_report["errors"]
        if err["type"] == "missing-label"
    ]

    ui_report["table"]["cols_alert"] = [
        "table-danger" if h not in converted_fields_dict or h in missing_headers else ""
        for h in converted_headers
    ]


def add_warnings_and_errors_counts(
    ui_report: Dict[str, Any],
    errors: List[Dict[str, str]],
    table_report: Dict[str, Any],
):
    """Add errors count and warnings coint to the UI report"""
    ui_report["error_count"] = len(errors)
    ui_report["warn_count"] = len(table_report["warnings"])
    ui_report["warnings"] = table_report["warnings"]


def group_errors_into_structure_and_body(
    ui_report: Dict[str, Any],
    errors: List[Dict[str, str]],
):
    """Group errors into two disctinct groups 'structure' and 'body'
    in the UI report
    """
    ui_report["table"]["errors"] = {"structure": [], "body": []}
    report_errors = ui_report["table"]["errors"]
    for err in errors:
        if is_structure_error(err):
            report_errors["structure"].append(err)
        elif is_body_error(err):
            report_errors["body"].append(err)


def group_body_errors_by_row_id(ui_report: Dict[str, Any]):
    """Group body errorsby row id in the Ui report"""
    rows: List[Dict] = []
    current_row_id = 0
    for err in ui_report["table"]["errors"]["body"]:
        if "rowNumber" not in err:
            continue
        row_id = err["rowNumber"]
        if row_id != current_row_id:
            current_row_id = row_id
            rows.append({"row_id": current_row_id, "errors": {}})

        column_id = err.get("fieldNumber")
        if column_id is not None:
            rows[-1]["errors"][column_id] = err
        else:
            rows[-1]["errors"]["row"] = err
    ui_report["table"]["errors"]["body_by_rows"] = rows


def sort_by_error_names_in_statistics(ui_report: Dict[str, Any]):
    """Sort by error names in statistics UI report"""
    ui_report["table"]["count-by-code"] = {}
    stats: Dict[str, Any] = {}
    total_errors_count = 0
    for key in ("structure", "body"):
        # convert dict into tuples with french title instead of error code
        # and sorts by title
        key_errors = ui_report["table"]["errors"][key]
        key_errors_count = len(key_errors)
        ct = Counter(ke["title"] for ke in key_errors)

        error_stats = {
            "count": key_errors_count,
            "count-by-code": sorted((k, v) for k, v in ct.items()),
        }
        total_errors_count += key_errors_count

        # Add error rows count
        if key == "body":
            error_rows = {err["rowNumber"] for err in key_errors if "rowNumber" in err}
            error_stats["rows-count"] = len(error_rows)

        stats[f"{key}-errors"] = error_stats

    stats["count"] = total_errors_count
    ui_report["table"]["error-stats"] = stats


def create_validata_ui_report(
    rows_count: int,
    formatted_validata_core_report: Dict[str, Any],
    schema_dict: Dict[str, Any],
    header_case: bool,
) -> Dict[str, Any]:
    """Create an error report easier to handle and display using templates.

    improvements done:
    - only one table
    - errors are contextualized
    - error-counts is ok
    - errors are grouped by lines
    - errors are separated into "structure" and "body"
    - error messages are improved
    """
    v_report = copy.deepcopy(formatted_validata_core_report)

    # Create a new UI report from information picked in validata report
    ui_report: Dict[str, Any] = {}
    ui_report["table"] = {}

    headers = v_report["tasks"][0]["labels"]

    add_source_headers_and_source_dimensions(ui_report, headers, rows_count)

    # Computes column info from schema
    fields_dict = {
        f["name"]: (f.get("title", f["name"]), f.get("description", ""))
        for f in schema_dict.get("fields", [])
    }

    add_header_titles_and_description(
        ui_report,
        fields_dict,
        header_case,
        headers,
    )

    v_report_table = v_report["tasks"][0]

    add_columns_alerts(
        v_report_table,
        ui_report,
        fields_dict,
        headers,
        header_case,
    )

    # prepare error structure for UI needs
    errors = build_ui_errors(v_report_table["errors"])

    add_warnings_and_errors_counts(ui_report, errors, v_report_table)

    group_errors_into_structure_and_body(ui_report, errors)

    group_body_errors_by_row_id(ui_report)

    sort_by_error_names_in_statistics(ui_report)

    return ui_report


def iter_task_errors(
    report: Report, code_set: Optional[Set[str]] = None
) -> Generator[Error, Any, Any]:
    """Iterate on errors that prevent optimal validation."""
    if report.tasks:
        yield from (
            err
            for err in report.tasks[0].errors
            if code_set is None or err.type in code_set
        )


def validate(
    schema_instance: SchemaInstance,
    validata_resource: ValidataResource,
    header_case: bool,
) -> Union[Response, str]:
    """Validate source and display report."""

    def compute_resource_info(resource: ValidataResource):
        source = resource.source()
        return {
            "type": "url" if source.startswith("http") else "file",
            "url": source,
            "filename": Path(source).name,
        }

    # Call validata_core with parsed data
    validata_core_report = validation_service.validate_resource(
        validata_resource, schema_instance.schema, header_case
    )

    formatted_validata_core_report = resource.to_dict(validata_core_report)

    # Handle pre-validation errors
    pre_validation_errors, redirected_url = handle_unviewable_errors(
        validata_resource, validata_core_report, schema_instance
    )

    if pre_validation_errors:
        return redirect(redirected_url)

    # # handle report date
    report_datetime = datetime.fromisoformat(
        formatted_validata_core_report["date"]
    ).astimezone()

    rows_count = len(validata_resource.rows())
    # create ui_report
    ui_report = create_validata_ui_report(
        rows_count, formatted_validata_core_report, schema_instance.schema, header_case
    )

    # Display report to the user
    validator_form_url = compute_validation_form_url(
        schema_instance.request_parameters()
    )
    schema_info = compute_schema_info(schema_instance.schema, schema_instance.url)

    return render_template(
        "validation_report.html",
        config=config,
        badge_msg=None,
        badge_url=None,
        breadcrumbs=[
            {"title": _("Accueil"), "url": url_for("home")},
            {"title": schema_instance.section_title},
            {"title": schema_info["title"], "url": validator_form_url},
            {"title": _("Rapport de validation")},
        ],
        display_badge=False,
        doc_url=schema_instance.doc_url,
        print_mode=request.args.get("print", "false") == "true",
        report=ui_report,
        schema_current_version=schema_instance.ref,
        schema_info=schema_info,
        section_title=schema_instance.section_title,
        source_data=build_template_source_data(
            validata_resource.header(), validata_resource.rows()
        ),
        resource=compute_resource_info(validata_resource),
        validation_date=report_datetime.strftime("le %d/%m/%Y à %Hh%M"),
    )


def handle_unviewable_errors(
    validata_resource: ValidataResource,
    validata_core_report: Report,
    schema_instance: SchemaInstance,
) -> Tuple[List[Error], str]:
    """This function aims to renders an explicte flash message error when some specific
    errors occure in the validation report which are unviewable in the data tabular visualization.
    Specific errors handled in this function are:
    - `Error` with this specific message '"schema_sync" requires unique labels in the header'
    - `SchemaError`
    - `CheckError
    - `SourceError`

    """

    pre_validation_errors = list(
        iter_task_errors(
            validata_core_report,
            {
                "error",
                "schema-error",
                "check-error",
                "source-error",
            },
        )
    )

    redirected_url = compute_validation_form_url(schema_instance.request_parameters())

    flash_message_error_set = set()

    for error in pre_validation_errors:
        # Error with duplicated labels in header
        if error.type == "error" and (
            '"schema_sync" requires unique labels in the header' in error.note
        ):
            flash_message_error_set.add(
                f"Le fichier '{Path(validata_resource.source()).name}' comporte des colonnes avec le même nom. "
                "Pour valider le fichier, veuillez d'abord le corriger en mettant des valeurs uniques dans "
                "son en-tête (la première ligne du fichier)."
            )

        # 'SchemaError' occurs in frictionless report in these cases :
        # - a field name does not exist in the schema
        # - a field name is not unique in the schema
        # - a primary key does not match the corresponding schema fields
        # - a foreign key does not match the corresponding schema fields
        # - foreign key fields does not match the reference fields
        if error.type == "schema-error":
            flash_message_error_set.add(
                "Erreur de schéma : Le schéma n'est pas valide selon la spécification TableSchema."
            )

        if error.type == "check-error":
            flash_message_error_set.add('Erreur de "custom_checks" : ' f"{error.note}")

        if error.type == "source-error":
            msg = (
                _("l'encodage du fichier est invalide. Veuillez le corriger.")
                if "charmap" in error.message
                else error.message
            )
            flash_message_error_set.add("Erreur de source : {}.".format(msg))
            redirected_url = url_for("custom_validator")

    flash_message_error = " - ".join(flash_message_error_set)

    if flash_message_error_set:
        flash_error(f"Validation annulée : {flash_message_error}")

    return pre_validation_errors, redirected_url


def bytes_data(f) -> bytes:
    """Get bytes data from Werkzeug FileStorage instance."""
    iob = io.BytesIO()
    f.save(iob)
    iob.seek(0)
    return iob.getvalue()


def retrieve_schema_catalog(
    section: Section,
) -> Tuple[Optional[SchemaCatalog], Optional[Dict[str, Any]]]:
    """Retrieve schema catalog and return formatted error if it fails."""

    def format_error_message(err_message: str, exc: Exception) -> str:
        """Prepare a bootstrap error message with details if wanted."""
        exception_text = "\n".join([str(arg) for arg in exc.args])

        return f"""{err_message}
        <div class="float-right">
            <button type="button" class="btn btn-info btn-xs" data-toggle="collapse"
                data-target="#exception_info">détails</button>
        </div>
        <div id="exception_info" class="collapse">
                <pre>{exception_text}</pre>
        </div>
"""

    try:
        schema_catalog = get_schema_catalog(section.name)
        return (schema_catalog, None)

    except Exception as exc:
        err_msg = "une erreur s'est produite"
        if isinstance(exc, requests.ConnectionError):
            err_msg = _("problème de connexion")
        elif isinstance(exc, json.decoder.JSONDecodeError):
            err_msg = _("format JSON incorrect")
        elif isinstance(exc, exceptions.ValidationError):
            err_msg = _("le catalogue ne respecte pas le schéma de référence")
        log.exception(err_msg)

        error_catalog = {
            **{k: v for k, v in section.dict().items() if k != "catalog"},
            "err": format_error_message(err_msg, exc),
        }
        return None, error_catalog


# Routes


def iter_sections() -> Iterable[Union[Section, Optional[Dict[str, Any]]]]:
    """Yield sections of the home page, filled with schema metadata."""
    # Iterate on all sections
    for section in config.CONFIG.homepage.sections:
        # section with only links to external validators
        if section.links:
            yield section
            continue

        # section with catalog
        if section.catalog is None:
            # skip section
            continue

        # retrieving schema catatalog
        schema_catalog, catalog_error = retrieve_schema_catalog(section)
        if schema_catalog is None:
            yield catalog_error
            continue

        # Working on catalog
        schema_info_list = []
        for schema_reference in schema_catalog.references:
            # retain tableschema only
            if schema_reference.get_schema_type() != "tableschema":
                continue

            # Loads default table schema for each schema reference
            schema_info: Dict[str, Any] = {"name": schema_reference.name}
            try:
                table_schema = fetch_schema(schema_reference.get_schema_url())
            except json.JSONDecodeError:
                schema_info["err"] = True
                schema_info["title"] = (
                    f"le format du schéma « {schema_info['name']} » "
                    "n'est pas reconnu"
                )
            except Exception:
                schema_info["err"] = True
                schema_info["title"] = (
                    f"le schéma « {schema_info['name']} » " "n'est pas disponible"
                )
            else:
                schema_info["title"] = table_schema.get("title") or schema_info["name"]
            schema_info_list.append(schema_info)
        schema_info_list = sorted(
            schema_info_list, key=lambda sc: strip_accents(sc["title"].lower())
        )

        yield {
            **{k: v for k, v in section.dict().items() if k != "catalog"},
            "catalog": schema_info_list,
        }


section_updater = ThreadUpdater(lambda: list(iter_sections()))


@app.route("/")
def home():
    """Home page."""

    return render_template("home.html", config=config, sections=section_updater.value)


def extract_schema_metadata(table_schema: dict) -> Dict[str, Any]:
    """Get author, contibutor, version...metadata from schema header."""
    return {k: v for k, v in table_schema.items() if k != "fields"}


def compute_schema_info(table_schema: dict, schema_url) -> Dict[str, Any]:
    """Factor code for validator form page."""
    # Schema URL + schema metadata info
    schema_info = {
        "path": schema_url,
        # a "path" metadata property can be found in Table Schema,
        # and we'd like it to override the `schema_url`
        # given by the user (in case schema was given by URL)
        **extract_schema_metadata(table_schema),
    }
    return schema_info


def compute_validation_form_url(request_parameters: Dict[str, Any]) -> str:
    """Compute validation form url with schema URL parameter."""
    url = url_for("custom_validator")
    return "{}?{}".format(url, urlencode(request_parameters))


def redirect_url_if_needed(url_param: str) -> str:
    """
    Redirects the url of url_param to its static url and
    returns this url.
    If url_param is already a static url, there is no
    url redirection, and it returns its value.

    :param url_param: str : url to redirect
    :return: str: redirected url
    """

    redirected_url = urlopen(url_param).geturl()
    return redirected_url


def get_header_case_from_checkbox(req: Request) -> bool:
    """
    Get the value of the "header-case" checkbox.
    The value is stored as a query string parameter or in the
    request body, depending on the method used for the form
    submit (GET or POST respectively).

    :return: bool: header_case (True if case-sensitive, False otherwise)
    """
    header_case = req.form.get("header-case", type=bool, default=False) or req.args.get(
        "header-case", type=bool, default=False
    )
    return header_case


@app.route("/table-schema", methods=["GET", "POST"])
def custom_validator() -> Union[str, Response, Tuple[str, int]]:
    """Display validator form."""
    if request.method == "GET":
        # input is a hidden form parameter to know
        # if this is the initial page display or if the validation has been asked for
        input_param = request.args.get("input")

        # url of resource to be validated
        url_param = request.args.get("url")

        schema_instance = SchemaInstance(request.args)

        try:
            schema_validation_report = validation_service.validate_schema(
                schema_instance.schema
            )
        except frictionless.exception.FrictionlessException as e:
            flash_error(f"Une erreur est survenue pendant la validation du schéma: {e}")
            return redirect(url_for("home"))

        errors = schema_validation_report.errors
        if errors:
            if "schema_url" in request.args:
                flash_error(
                    "Le schéma fourni est invalide.\n"
                    f"Erreurs survenues lors de la validation : {  [e.message for e in errors] }"
                )
                return redirect(url_for("home"))

            elif "schema_name" in request.args:
                flash_error(
                    f"Le schéma choisi '{schema_instance.schema['title']}', "
                    f"version '{schema_instance.schema['version']}' est invalide. La validation de "
                    f"données est impossible pour cette version '{schema_instance.schema['version']}'. "
                    "Veuillez choisir une autre version."
                )
                return redirect(
                    compute_validation_form_url(
                        {
                            "schema_name": schema_instance.request_parameters()[
                                "schema_name"
                            ],
                            "schema_ref": "master",
                        }
                    )
                )
            else:
                return redirect(url_for("home"))

        # First form display
        if input_param is None:
            schema_info = compute_schema_info(
                schema_instance.schema,
                schema_instance.url,
            )
            return render_template(
                "validation_form.html",
                config=config,
                branches=schema_instance.branches,
                breadcrumbs=[
                    {"url": url_for("home"), "title": "Accueil"},
                    {"title": schema_instance.section_title},
                    {"title": schema_info["title"]},
                ],
                doc_url=schema_instance.doc_url,
                schema_current_version=schema_instance.ref,
                schema_info=schema_info,
                schema_params=schema_instance.request_parameters(),
                section_title=schema_instance.section_title,
                tags=schema_instance.tags,
            )

        # Process URL
        else:
            validation_form_url = compute_validation_form_url(
                schema_instance.request_parameters()
            )

            if not url_param:
                flash_error(_("Vous n'avez pas indiqué d'URL à valider"))
                return redirect(validation_form_url)
            try:
                url = redirect_url_if_needed(url_param)
                validata_resource = resource.from_remote_file(url)
            except Exception as ex:
                flash_error(
                    f"Une erreur s'est produite en récupérant les données : {ex}"
                )
                return redirect(validation_form_url)

            try:
                header_case = get_header_case_from_checkbox(request)
                return validate(
                    schema_instance, validata_resource, header_case=header_case
                )
            except Exception as ex:
                flash_error(f"Une erreur s'est produite en validant les données : {ex}")
                return redirect(validation_form_url)

    elif request.method == "POST":
        schema_instance = SchemaInstance(request.form)

        input_param = request.form.get("input")
        if input_param is None:
            flash_error(_("Vous n'avez pas indiqué de fichier à valider"))
            return redirect(
                compute_validation_form_url(schema_instance.request_parameters())
            )

        # File validation
        if input_param == "file":
            f = request.files.get("file")
            if f is None:
                flash_warning(_("Vous n'avez pas indiqué de fichier à valider"))
                return redirect(
                    compute_validation_form_url(schema_instance.request_parameters())
                )
            try:
                validata_resource = resource.from_file_content(
                    f.filename or "", bytes_data(f)
                )
            except Exception as err:
                flash_error(
                    f"Une erreur s'est produite à l'extraction de l'en-tête et des lignes du fichier. Veuillez vérifier que le fichier est valide. Erreur : {err}"
                )
                return redirect(
                    compute_validation_form_url(schema_instance.request_parameters())
                )
            header_case = get_header_case_from_checkbox(request)
            return validate(schema_instance, validata_resource, header_case=header_case)

        return _("Combinaison de paramètres non supportée"), 400

    else:
        return "Method not allowed", 405
