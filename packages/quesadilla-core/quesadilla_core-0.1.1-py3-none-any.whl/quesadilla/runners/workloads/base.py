# `quesadilla` - an elegant background task queue for the more civilized age
# Copyright (C) 2024 Artur Ciesielski <artur.ciesielski@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from dataclasses import dataclass, field
from functools import cached_property

import ulid

from quesadilla.core.task_queues import GenericQueuedTask, TaskQueue
from quesadilla.runners.runners.protocol import Event, Runner
from quesadilla.runners.workloads.protocol import (
    ExecutedQueuedTaskLoggingExtras,
    Workload,
    WorkloadLoggingExtras,
)


@dataclass(frozen=True)
class BaseWorkload(Workload):
    runner: Runner
    task_queue: TaskQueue

    id: ulid.ULID = field(default_factory=ulid.ULID, init=False)

    closed: Event = field(kw_only=True, repr=False)
    stopped: Event = field(kw_only=True, repr=False)

    logger: logging.Logger = field(init=False, repr=False)

    @cached_property
    def logging_extras(self) -> WorkloadLoggingExtras:
        return {
            "task_queue": self.task_queue.logging_extras,
            "id": str(self.id),
            "runner": self.runner.logging_extras,
        }

    def __post_init__(self) -> None:
        super().__setattr__("logger", logging.getLogger(self.name))

    def get_queued_task_logging_extras(
        self, queued_task: GenericQueuedTask
    ) -> ExecutedQueuedTaskLoggingExtras:
        return {
            **queued_task.logging_extras,
            "workload": self.logging_extras,
        }

    def close(self):
        self.closed.set()

    def stop(self):
        self.stopped.set()
