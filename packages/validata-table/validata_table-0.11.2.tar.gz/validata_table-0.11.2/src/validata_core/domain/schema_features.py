from pathlib import Path
from typing import Dict, List, Union

from validata_core.domain.spi import (
    LocalContentFetcher,
    RemoteContentFetcher,
    TableSchemaService,
)
from validata_core.domain.types import (
    JSON,
    CustomCheck,
    CustomCheckError,
    Error,
    Schema,
    SchemaDescriptor,
)
from validata_core.domain.types.utils import Res


def fetch_remote_descriptor(
    url: str, remote_content_fetcher: RemoteContentFetcher
) -> Res[SchemaDescriptor, Error]:
    return remote_content_fetcher.fetch(url)


def fetch_local_descriptor(
    filepath: Union[str, Path], local_content_fetcher: LocalContentFetcher
) -> Res[SchemaDescriptor, Error]:
    return local_content_fetcher.fetch(filepath)


def parse(
    descriptor: SchemaDescriptor, table_schema_service: TableSchemaService
) -> Res[Schema, Error]:
    schema, err = table_schema_service.parse(descriptor)

    if err:
        return schema, err

    if "custom_checks" in descriptor:
        custom_checks, err = _to_custom_checks(descriptor["custom_checks"])

        if err:
            return schema, err

        schema.custom_checks = custom_checks

    return schema, None


def _to_custom_checks(checks_descriptor: JSON) -> Res[List[CustomCheck], Error]:
    if not isinstance(checks_descriptor, List):
        return [], CustomCheckError(
            note='The "custom_checks" property expects a JSON array. Got:\n{checks_descriptor}'
        )

    custom_checks: List[CustomCheck] = []

    for check in checks_descriptor:
        if not isinstance(check, Dict):
            return [], CustomCheckError(
                note=f'Each element of the "custom_checks" array is expected to be a JSON object. Got:\n{check}'
            )

        if "name" not in check:
            return [], CustomCheckError(
                note=f'Each element custom check is expected to have a "name" property. Got:\n{check}'
            )

        if not isinstance(check["name"], str):
            return [], CustomCheckError(
                note=f'The "name" property of a custom check is expected to be a string. Got:\n{check["name"]}'
            )

        if "params" not in check:
            return [], CustomCheckError(
                note=f'Each element custom check is expected to have a "params" property. Got:\n{check}'
            )

        if not isinstance(check["params"], Dict):
            return [], CustomCheckError(
                note=f'The "params" property of a custom check is expected to be a JSON object. Got:\n{check["params"]}'
            )

        custom_checks.append(CustomCheck(check["name"], check["params"]))

    return custom_checks, None
