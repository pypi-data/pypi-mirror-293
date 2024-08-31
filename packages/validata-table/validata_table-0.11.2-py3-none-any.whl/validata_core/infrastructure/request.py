import json
from typing import Optional

import requests

from validata_core.domain.spi import RemoteContentFetcher, RequestService
from validata_core.domain.types import Error, SchemaDescriptor
from validata_core.domain.types.utils import Res


class Requests(RequestService):
    def get_content_type_header(self, url: str) -> Optional[str]:
        try:
            response = requests.head(url)

            return response.headers.get("Content-Type")
        except requests.RequestException:
            return None


class RequestsContentFetcher(RemoteContentFetcher):
    def fetch(self, url: str) -> Res[SchemaDescriptor, Error]:
        response = requests.get(url)
        schema_descriptor = json.loads(response.text)

        return schema_descriptor, None
