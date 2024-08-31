import frictionless
import frictionless.errors as frerr

from validata_core.domain.spi import TableSchemaService
from validata_core.domain.types import Error
from validata_core.domain.types.field import Field
from validata_core.domain.types.schema import Schema, SchemaDescriptor
from validata_core.domain.types.utils import Res


class FrlessTableSchemaService(TableSchemaService):
    def parse(self, descriptor: SchemaDescriptor) -> Res[Schema, Error]:
        try:
            schema = frictionless.Schema.from_descriptor(descriptor)
            return Schema(descriptor, [Field(f) for f in schema.fields], []), None
        except frictionless.FrictionlessException as e:
            err = frerr.FormatError(note="Trying to parse an invalid schema")
            err.__cause__ = e
            return Schema(descriptor, [], []), Error(err)
