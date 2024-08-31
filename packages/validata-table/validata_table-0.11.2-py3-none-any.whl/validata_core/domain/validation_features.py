import logging
from pathlib import Path
from typing import Union

import validata_core.domain.schema_features as schema_features
from validata_core.domain.custom_checks_interface import build_custom_checks
from validata_core.domain.error_messages import FrLocale, Locale, translate_errors
from validata_core.domain.resource_features import ResourceFeatures
from validata_core.domain.spi import (
    CustomFormatsRepository,
    LocalContentFetcher,
    RemoteContentFetcher,
    TableSchemaService,
    ValidationService,
)
from validata_core.domain.types import (
    Report,
    Schema,
    SchemaDescriptor,
    Source,
    ValidataResource,
)


class ValidationFeatures:
    def __init__(
        self,
        validation_service: ValidationService,
        table_schema_service: TableSchemaService,
        resource_features: ResourceFeatures,
        remote_content_fetcher: RemoteContentFetcher,
        local_content_fetcher: LocalContentFetcher,
        custom_formats_repository: CustomFormatsRepository,
    ):
        self._validation_service = validation_service
        self._resource_features = resource_features
        self._table_schema_service = table_schema_service
        self._remote_content_fetcher = remote_content_fetcher
        self._local_content_fetcher = local_content_fetcher
        self._custom_formats_repository = custom_formats_repository

    def validate_schema(
        self,
        schema_descriptor: SchemaDescriptor,
    ) -> Report:
        return self._validation_service.validate_schema(schema_descriptor)

    def validate(
        self,
        source: Source,
        schema_descriptor: Union[SchemaDescriptor, str],
        header_case: bool = True,
        **options,
    ) -> Report:
        """
        Validate a `source` using a `schema` returning a validation report.

        `source` and `schema` can be access paths to local or remote files, or
        already parsed into python.
        """

        resource: ValidataResource = self._resource_features.make_validata_resource(
            source
        )

        return self.validate_resource(
            resource, schema_descriptor, header_case, **options
        )

    def validate_resource(
        self,
        resource: ValidataResource,
        schema_descriptor: Union[SchemaDescriptor, str, Path],
        header_case: bool = True,
        **options,
    ) -> Report:
        schema_validation_report = self._validation_service.validate_schema(
            schema_descriptor
        )

        if not schema_validation_report.valid:
            return schema_validation_report

        if isinstance(schema_descriptor, str) and schema_descriptor.startswith("http"):
            schema_descriptor, err = schema_features.fetch_remote_descriptor(
                schema_descriptor, self._remote_content_fetcher
            )
            if err:
                schema_validation_report.add_errors([err])

        if isinstance(schema_descriptor, str) or isinstance(schema_descriptor, Path):
            schema_descriptor, err = schema_features.fetch_local_descriptor(
                schema_descriptor, self._local_content_fetcher
            )
            if err:
                schema_validation_report.add_errors([err])

        schema, err = schema_features.parse(
            schema_descriptor, self._table_schema_service
        )

        if err:
            schema_validation_report.add_errors([err])
            return schema_validation_report

        # Build checks and related errors from schema
        (
            custom_checks,
            check_errors,
        ) = build_custom_checks(schema, self._custom_formats_repository)

        report: Report = self._validation_service.validate(
            resource=resource,
            schema=schema,
            checks=custom_checks,
            header_case_sensitive=header_case,
        )

        report.add_errors(check_errors)

        translate_report(report, schema, FrLocale())

        return report


log = logging.getLogger(__name__)


def translate_report(report: Report, schema: Schema, locale: Locale):
    """
    Translate errors contained in the validation report in french langage.
    """
    report.errors = translate_errors(report.errors, schema, locale)

    for tasks in report.tasks:
        tasks.errors = translate_errors(tasks.errors, schema, locale)
