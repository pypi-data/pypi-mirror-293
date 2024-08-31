from typing import Any, Dict

import frictionless

from validata_core.domain.spi import ToDictService
from validata_core.domain.types import Report, Schema, Task, ValidataResource
from validata_core.infrastructure.frictionless_validation import (
    _consolidate_to_frless_resource,
)


class FrictionlessToDictService(ToDictService):
    # Not very elegant, but encapsulates the current dependency to
    # frictionless for the conversion
    def report_to_dict(self, report: Report) -> Dict[str, Any]:
        """Overwrites frictionless.metadata to_dict().
        Returns a dict containing all Report object's properties information.
        """

        report_dict = report.frless_report.to_dict()

        report_dict["date"] = report.date

        report_dict["errors"] = [
            error.to_dict(dict_error)
            for error, dict_error in zip(report.errors, report_dict["errors"])
        ]

        report_dict["tasks"] = [
            self._improve_frless_task_dict(task, task_dict) if task else {}
            for task, task_dict in zip(report.tasks, report_dict["tasks"])
        ]
        report_dict["time"] = report.time  # Deprecated
        report_dict["version"] = report.version

        return report_dict

    def _improve_frless_task_dict(
        self, task: Task, frless_task_dict: Dict
    ) -> Dict[str, Any]:
        """Overwrites frictionless.metadata to_dict().
        Returns a dict containing all Task object's properties information with added
        some deprecated information linked to this task.
        """
        dict_task = frless_task_dict
        dict_task["errors"] = [
            error.to_dict(dict_error)
            for error, dict_error in zip(task.errors, dict_task["errors"])
        ]

        # All following key-values are deprecated in frictionless
        # but kept in this class for retrocompatibility
        dict_task["partial"] = task.partial
        dict_task["scope"] = task.scope
        dict_task["structure_warnings"] = task.structure_warnings
        dict_task["time"] = task.time
        if task.resource:
            dict_task["resource"] = self._improve_frless_resource_dict(
                task.resource, task.original_schema, task.header_case_sensitive
            )
        return dict_task

    def _improve_frless_resource_dict(
        self, resource: ValidataResource, schema: Schema, header_case_sensitive: bool
    ) -> Dict[str, Any]:
        """Create and returns a dict containing informations attributes
        of the frictionless Resource object given in parameter with added
        some deprecated information linked to this resource.
        """
        frless_schema = frictionless.Schema(schema.descriptor)

        frless_resource = _consolidate_to_frless_resource(
            resource, frless_schema, header_case_sensitive
        )

        dict_resource = frless_resource.to_dict()

        frless_resource_for_stats = frless_resource.to_copy()
        frless_resource_for_stats.infer(stats=True)

        frless_resource.stats = frless_resource_for_stats.stats

        # Edit task_resource schema with original schema as the resource's schema is modified by frictionless at its creation
        dict_resource["schema"] = frless_schema.to_dict()

        # All following key-values are deprecated in frictionless
        # but kept in this class for retrocompatibility
        dict_resource["layout"] = {
            "headerCase": frless_resource.dialect.header_case,
            "limitRows": 100000,
        }
        dict_resource["hashing"] = "deprecated"
        dict_resource["profile"] = "deprecated"
        dict_resource["scheme"] = "deprecated"
        dict_resource["stats"] = {
            "bytes": frless_resource.bytes if frless_resource.bytes else "deprecated",
            "fields": len(frless_schema.fields),
            "hash": "deprecated",
            "rows": frless_resource.stats.rows,
        }

        return dict_resource
