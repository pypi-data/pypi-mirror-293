from typing import Any, Dict, List, Optional, Union

import frictionless

from validata_core.domain.structure_warnings import iter_structure_warnings
from validata_core.domain.types.schema import Schema

from .error import Error
from .resource import ValidataResource


class Task:
    def __init__(
        self,
        task: frictionless.ReportTask,
        resource: Optional[ValidataResource],
        errors: List[frictionless.Error],
        original_schema: Schema,
        header_case_sensitive: bool,
    ):
        # Init Task object with frictionless.Task object's properties
        self.name = task.name
        self.type = task.type
        self.title = task.title
        self.description = task.description
        self.valid = task.valid
        self.place = task.place
        self.labels = task.labels
        self.stats = task.stats
        self.warnings = task.warnings
        self.header_case_sensitive = header_case_sensitive

        # Edit Task object ihnerited frictionless.Task object's properties :
        # Edit task_stats fields with original schema data as the task is built on resource's schema which is modified by frictionless at its creation
        self.stats["fields"] = len(original_schema.fields) if original_schema else 0
        self.errors: List[Error] = [Error(err) for err in errors]

        # Add specific new attributes the Task object, most of them are deprecated
        self.frless_task: frictionless.ReportTask = task
        self.original_schema: Schema = original_schema

        ## All following attributes are deprecated in frictionless
        ## but kept in this class for retrocompatibility
        self.resource: Optional[ValidataResource] = resource
        self.scope: List[str] = [
            "hash-count-error",
            "byte-count-error",
            "field-count-error",
            "row-count-error",
            "blank-header",
            "extra-label",
            "missing-label",
            "blank-label",
            "duplicate-label",
            "incorrect-label",
            "blank-row",
            "primary-key-error",
            "foreign-key-error",
            "extra-cell",
            "missing-cell",
            "type-error",
            "constraint-error",
            "unique-error",
        ]
        self.partial: bool = False
        self.structure_warnings: list[Union[Dict[str, str], Any, None]] = [
            iter_structure_warnings(warning) for warning in self.warnings
        ]
        self.time: Union[float, int] = task.stats["seconds"]
