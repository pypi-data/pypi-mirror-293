import functools
from typing import Callable

from validata_core.domain.resource_features import ResourceFeatures
from validata_core.domain.types import Report
from validata_core.domain.validation_features import ValidationFeatures
from validata_core.infrastructure.fr_formats import FrFormatsRepository
from validata_core.infrastructure.frictionless_validation import (
    FrictionlessValidationService,
)
from validata_core.infrastructure.request import Requests, RequestsContentFetcher
from validata_core.infrastructure.resource_readers import (
    FrictionlessFileContentService,
    FrictionlessInlineContentService,
    FrictionlessRemoteFileService,
    LocalContentReader,
)
from validata_core.infrastructure.resource_to_dict import FrictionlessToDictService
from validata_core.infrastructure.table_schema_service import FrlessTableSchemaService

# Resources

file_content_service = FrictionlessFileContentService()
remote_file_service = FrictionlessRemoteFileService(Requests())
inline_content_service = FrictionlessInlineContentService()
to_dict_service = FrictionlessToDictService()

resource_service = ResourceFeatures(
    file_content_service,
    remote_file_service,
    inline_content_service,
    to_dict_service,
)

# Validation

frictionless_validation_service = FrictionlessValidationService()
frictionless_table_schema_service = FrlessTableSchemaService()
remote_content_fetcher = RequestsContentFetcher()
local_content_fetcher = LocalContentReader()
custom_formats_repository = FrFormatsRepository()

validation_service = ValidationFeatures(
    frictionless_validation_service,
    frictionless_table_schema_service,
    resource_service,
    remote_content_fetcher,
    local_content_fetcher,
    custom_formats_repository,
)

ValidateSignature = Callable[..., Report]

validate: ValidateSignature = functools.partial(
    validation_service.validate.__func__,  # type: ignore
    validation_service,
)
validate_schema = functools.partial(
    validation_service.validate_schema.__func__,  # type: ignore
    validation_service,
)
