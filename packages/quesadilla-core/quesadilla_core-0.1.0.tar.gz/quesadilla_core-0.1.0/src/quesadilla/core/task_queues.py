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

from __future__ import annotations

import asyncio
import datetime
import time
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, Self

import ulid

from quesadilla.connectors.protocol import Connector
from quesadilla.core.errors import (
    DuplicateTaskNameError,
    DuplicateTaskQueueNameError,
    TaskDoesNotExistAnymoreError,
    TaskNotFinishedError,
    UnknownTaskNameError,
)
from quesadilla.core.logging import QueuedTaskLoggingExtras, TaskQueueLoggingExtras
from quesadilla.core.task_executables import Failure, Success, TaskExecutable
from quesadilla.core.task_metadata import BaseTaskMetadata, SerializableTask


@dataclass(frozen=True)
class TaskQueue:
    name: str
    namespace: str | None = None

    connector: Connector = field(kw_only=True, repr=False)
    task_executables: MutableMapping[str, TaskExecutable[Any, Any]] = field(
        default_factory=dict, init=False, repr=False
    )

    def register_task_executable(
        self, task_executable: TaskExecutable[Any, Any]
    ) -> None:
        if task_executable.name in self.task_executables:
            raise DuplicateTaskNameError(
                namespace=self.namespace,
                task_queue_name=self.name,
                task_name=task_executable.name,
            )
        self.task_executables[task_executable.name] = task_executable

    def get_task_executable(self, name: str) -> TaskExecutable[Any, Any]:
        try:
            return self.task_executables[name]
        except KeyError as e:
            raise UnknownTaskNameError(
                namespace=self.namespace,
                task_queue_name=self.name,
                task_name=name,
            ) from e

    def queue(self, queued_task: GenericQueuedTask) -> None:
        self.connector.queue(queued_task.serializable.serialize())

    async def aqueue(self, queued_task: GenericQueuedTask) -> None:
        await self.connector.aqueue(queued_task.serializable.serialize())

    def find(self, task_id: ulid.ULID) -> GenericQueuedTask | None:
        if (s := self.connector.find(self.namespace, self.name, task_id)) is None:
            return None

        return GenericQueuedTask.from_serializable(
            (serializable := SerializableTask.deserialize(s)),
            task_queue=self,
            task_executable=self.get_task_executable(serializable.task_name),
        )

    async def afind(self, task_id: ulid.ULID) -> GenericQueuedTask | None:
        if (
            s := await self.connector.afind(self.namespace, self.name, task_id)
        ) is None:
            return None

        return GenericQueuedTask.from_serializable(
            (serializable := SerializableTask.deserialize(s)),
            task_queue=self,
            task_executable=self.get_task_executable(serializable.task_name),
        )

    def pull(self) -> GenericQueuedTask | None:
        if (s := self.connector.pull(self.namespace, self.name)) is None:
            return None

        return GenericQueuedTask.from_serializable(
            (serializable := SerializableTask.deserialize(s)),
            task_queue=self,
            task_executable=self.get_task_executable(serializable.task_name),
        )

    def update(self, queued_task: GenericQueuedTask) -> None:
        self.connector.update(
            self.namespace, self.name, queued_task.serializable.serialize()
        )

    @cached_property
    def logging_extras(self) -> TaskQueueLoggingExtras:
        return {
            "namespace": self.namespace,
            "task_queue_name": self.name,
        }


@dataclass(frozen=True)
class TaskQueues:
    namespace: str
    connector: Connector

    task_queues: MutableMapping[str, TaskQueue] = field(
        default_factory=dict, init=False, repr=False
    )

    def new(self, name: str) -> TaskQueue:
        if name in self.task_queues:
            raise DuplicateTaskQueueNameError(
                namespace=self.namespace,
                task_queue_name=name,
            )

        task_queue = TaskQueue(name, namespace=self.namespace, connector=self.connector)
        self.task_queues[name] = task_queue

        return task_queue


@dataclass(frozen=True)
class GenericQueuedTask(BaseTaskMetadata[Any]):
    task_queue: TaskQueue = field(kw_only=True)
    task_executable: TaskExecutable[Any, Any] = field(kw_only=True)

    @cached_property
    def serializable(self) -> SerializableTask[Any]:
        return SerializableTask(
            id=self.id,
            namespace=self.task_queue.namespace,
            task_queue_name=self.task_queue.name,
            task_name=self.task_executable.name,
            execution_context=self.execution_context,
            execution_result=self.execution_result,
            queued_at=self.queued_at,
            started_at=self.started_at,
            finished_at=self.finished_at,
        )

    @classmethod
    def from_serializable(
        cls,
        serializable: SerializableTask[Any],
        task_queue: TaskQueue,
        task_executable: TaskExecutable[Any, Any],
    ) -> Self:
        return cls(
            id=serializable.id,
            task_queue=task_queue,
            task_executable=task_executable,
            execution_context=serializable.execution_context,
            execution_result=serializable.execution_result,
            queued_at=serializable.queued_at,
            started_at=serializable.started_at,
            finished_at=serializable.finished_at,
        )

    @cached_property
    def result(self) -> Success[Any] | Failure:
        if not self.execution_result.finished:
            raise TaskNotFinishedError(
                namespace=self.task_queue.namespace,
                task_queue_name=self.task_queue.name,
                task_name=self.task_executable.name,
                task_id=self.id,
            )

        if self.execution_result.exc is not None:
            return Failure(self.execution_result.exc)
        return Success(self.execution_result.value)

    def refresh(self) -> GenericQueuedTask:
        if (queued_task := self.task_queue.find(self.id)) is None:
            raise TaskDoesNotExistAnymoreError(
                namespace=self.task_queue.namespace,
                task_queue_name=self.task_queue.name,
                task_name=self.task_executable.name,
                task_id=self.id,
            )
        return queued_task

    async def arefresh(self) -> GenericQueuedTask:
        if (queued_task := await self.task_queue.afind(self.id)) is None:
            raise TaskDoesNotExistAnymoreError(
                namespace=self.task_queue.namespace,
                task_queue_name=self.task_queue.name,
                task_name=self.task_executable.name,
                task_id=self.id,
            )
        return queued_task

    def wait_for(self, interval: float = 0.1) -> GenericQueuedTask:
        while not (cursor := self.refresh()).finished:
            time.sleep(interval)
        return cursor

    async def await_for(self, interval: float = 0.1) -> GenericQueuedTask:
        while not (cursor := await self.arefresh()).finished:
            await asyncio.sleep(interval)
        return cursor

    def execute(self, asyncio_runner: asyncio.Runner) -> GenericQueuedTask:
        return GenericQueuedTask(
            id=self.id,
            task_queue=self.task_queue,
            task_executable=self.task_executable,
            execution_context=self.execution_context,
            execution_result=self.task_executable.execute(
                asyncio_runner,
                *self.execution_context.args,
                *self.execution_context.kwargs,
            ),
            queued_at=self.queued_at,
            started_at=self.started_at,
            finished_at=self.finished_at,
        )

    def start(self) -> GenericQueuedTask:
        return GenericQueuedTask(
            id=self.id,
            task_queue=self.task_queue,
            task_executable=self.task_executable,
            execution_context=self.execution_context,
            execution_result=self.execution_result,
            queued_at=self.queued_at,
            started_at=datetime.datetime.now(datetime.UTC),
            finished_at=self.finished_at,
        )

    def reset(self) -> GenericQueuedTask:
        return GenericQueuedTask(
            id=self.id,
            task_queue=self.task_queue,
            task_executable=self.task_executable,
            execution_context=self.execution_context,
            execution_result=self.execution_result,
            queued_at=self.queued_at,
            started_at=None,
            finished_at=None,
        )

    def finalize(self) -> GenericQueuedTask:
        return GenericQueuedTask(
            id=self.id,
            task_queue=self.task_queue,
            task_executable=self.task_executable,
            execution_context=self.execution_context,
            execution_result=self.execution_result,
            queued_at=self.queued_at,
            started_at=self.started_at,
            finished_at=datetime.datetime.now(datetime.UTC),
        )

    @cached_property
    def logging_extras(self) -> QueuedTaskLoggingExtras:
        return {
            "task_queue": self.task_queue.logging_extras,
            "task_name": self.task_executable.name,
            "id": str(self.id),
            "finished": self.execution_result.finished,
        }
