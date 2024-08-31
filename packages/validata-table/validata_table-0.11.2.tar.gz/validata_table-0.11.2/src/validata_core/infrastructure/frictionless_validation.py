from pathlib import Path
from typing import List, Optional

import frictionless
from frictionless.resources import TableResource

from validata_core.domain.spi import ValidationService
from validata_core.domain.types import (
    Error,
    InlineArrayOfArrays,
    Report,
    Schema,
    Task,
    ValidataResource,
    ValidataSourceError,
)
from validata_core.domain.warning_messages import iter_warnings
from validata_core.infrastructure.resource_readers import (
    _extract_header_and_rows_from_resource,
)


class FrictionlessValidationService(ValidationService):
    def validate(self, resource, schema, checks, header_case_sensitive) -> Report:
        frless_schema = frictionless.Schema.from_descriptor(schema.descriptor)

        original_schema = frless_schema.to_copy()

        consolidated_resource = _consolidate_to_frless_resource(
            resource, frless_schema, header_case_sensitive
        )

        source_header = None
        report = frictionless.validate(source=consolidated_resource, checks=checks)

        if report.tasks:
            try:
                source_header, _ = _extract_header_and_rows_from_resource(
                    consolidated_resource
                )
            except ValidataSourceError:
                source_header = None

        required_field_names = extract_required_field_names(frless_schema)

        for table in report.tasks:
            # Add warnings

            if source_header:
                table.warnings = list(
                    iter_warnings(
                        source_header,
                        required_field_names,
                        original_schema,
                        header_case_sensitive,
                    )
                )
                table.stats["warnings"] += len(table.warnings)
                report.stats["warnings"] += len(table.warnings)
                report.warnings += table.warnings

        formatted_report = format_report(
            report,
            resource,
            schema,
            header_case_sensitive,
        )
        return formatted_report

    def validate_schema(self, schema_descriptor):
        try:
            if isinstance(schema_descriptor, Path):
                schema_descriptor = str(schema_descriptor)
            frictionless.Schema.from_descriptor(schema_descriptor)
        except frictionless.FrictionlessException as exception:
            errors = exception.reasons if exception.reasons else [exception.error]
            return format_report(
                frictionless.Report.from_validation(errors=errors), None, None, False
            )

        frictionless_report = frictionless.validate(schema_descriptor, type="schema")
        return format_report(frictionless_report, None, None, False)


def _consolidate_to_frless_resource(
    resource: ValidataResource, schema: frictionless.Schema, header_case_sensitive: bool
) -> TableResource:
    resource_data: InlineArrayOfArrays = [resource.header()] + resource.rows()
    # Merge options to pass to frictionless
    frless_resource = TableResource(
        resource_data,
        schema=schema,
        dialect=frictionless.Dialect(header_case=header_case_sensitive),
        detector=frictionless.Detector(schema_sync=True),
    )

    return frless_resource


def extract_required_field_names(
    schema: frictionless.Schema,
) -> list[str]:
    return [
        field.name
        for field in schema.fields
        if field.constraints
        and "required" in field.constraints
        and field.constraints["required"]
    ]


def format_report(
    report: frictionless.Report,
    resource: Optional[ValidataResource],
    original_schema: Optional[Schema],
    header_case_sensitive: bool,
) -> Report:
    """This function aims to format the validata_core validation report
    into a dict form and transform it by adding all missing properties which
    were contained in validation report form when using frictionless v4.38.0
    but not existing using frictionless v5.16.
    These properties are added in order that Validata still is retrocompatible
    with upgrading to the v5 of frictionless.
    These added properties are now depreciated and mentionned as well in the
    returned dict. They will be removed in the future.
    """

    # Create errors from frictionless report
    formatted_errors = [Error(err) for err in report.errors]

    # Create tasks content from frictionless report
    formatted_tasks = []
    if original_schema:
        formatted_tasks = _create_tasks_contents_for_formatted_report(
            report, resource, original_schema, header_case_sensitive
        )

    formatted_report = Report(report, formatted_errors, formatted_tasks)

    return formatted_report


def _create_tasks_contents_for_formatted_report(
    report: frictionless.Report,
    resource: Optional[ValidataResource],
    original_schema: Schema,
    header_case_sensitive: bool,
) -> List[Task]:
    """This function aims to complete each tasks contained in the formatted report
    with all the task properties which were contained in an task report object in version
    4.38.0 of frictionless.
    """

    formatted_tasks = []

    for task in report.tasks:
        # Build task errors
        formatted_tasks.append(
            Task(task, resource, task.errors, original_schema, header_case_sensitive)
        )

    return formatted_tasks
