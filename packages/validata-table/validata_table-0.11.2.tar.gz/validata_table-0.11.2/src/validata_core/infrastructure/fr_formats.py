import re
from typing import List

from frformat import all_formats

from validata_core.domain.spi import CustomFormatsRepository
from validata_core.domain.types import Validator


class FrFormatsRepository(CustomFormatsRepository):
    @classmethod
    def formats_by_code(cls):
        return {
            _pascal_to_kebab_case(format.__name__): format for format in all_formats
        }

    def ls(self) -> List[str]:
        return list(self.formats_by_code().keys())

    def get_validator(self, format: str) -> Validator:
        if format in self.formats_by_code():

            def validate(value, **options):
                format_cls = self.formats_by_code()[format]
                return format_cls.is_valid(value, **options), ""

            return validate

        return lambda value, **options: (True, "")

    def get_description(self, format: str) -> str:
        return self.formats_by_code()[format].metadata.description


def _pascal_to_kebab_case(name):
    """Not flawless, but avoids a dependency"""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1-\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1-\2", name).lower()
