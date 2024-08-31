from datetime import datetime, timezone
from importlib.metadata import version
from typing import List, Optional

import frictionless
from frictionless.report.types import IReportStats

from .error import Error
from .task import Task


class Report:
    date: str
    errors: List[Error]
    version: str
    tasks: List[Task]
    frless_report: frictionless.Report

    def __init__(
        self,
        report: frictionless.Report,
        errors: List[Error],
        tasks: List[Task],
    ):
        # Edit report object ihnerited frictionless.Report object's properties
        self.errors = errors
        self.tasks = tasks

        # Add specific new properties the Report object
        self.frless_report = report
        self.date = datetime.now(timezone.utc).isoformat()
        self.version = version("frictionless")
        self.time = report.stats["seconds"]  # Deprecated

    def add_errors(self, errors: List[Error], root_level: bool = False):
        """Add errors to an existing report

        Frictionless differenciates root-level errors and task errors. The
        root level argument allows to control where to add errors, despite not
        supporting multiple tasks at once in Validata.
        """

        if errors:
            if root_level:
                self.errors.extend(errors)
            else:
                for task in self.tasks:
                    task.errors.extend(errors)
                    task.stats["errors"] += len(errors)

            self.stats["errors"] += len(errors)
            self.valid = False

    @property
    def valid(self) -> bool:
        return self.frless_report.valid

    @valid.setter
    def valid(self, value: bool):
        self.frless_report.valid = value

    @property
    def stats(self) -> IReportStats:
        return self.frless_report.stats

    @stats.setter
    def stats(self, value: IReportStats):
        self.frless_report.stats = value

    @property
    def name(self) -> Optional[str]:
        return self.frless_report.name

    @name.setter
    def name(self, value: str):
        self.frless_report.name = value

    @property
    def title(self) -> Optional[str]:
        return self.frless_report.title

    @title.setter
    def title(self, value: str):
        self.frless_report.title = value

    @property
    def description(self) -> Optional[str]:
        return self.frless_report.description

    @description.setter
    def description(self, value: str):
        self.frless_report.description = value

    @property
    def warnings(self) -> list:
        return self.frless_report.warnings

    @warnings.setter
    def warnings(self, value: list):
        self.frless_report.warnings = value
