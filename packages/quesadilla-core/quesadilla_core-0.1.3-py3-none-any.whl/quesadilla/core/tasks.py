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
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

import ulid

from quesadilla.core.errors import TaskDoesNotExistAnymoreError, TaskNotFinishedError
from quesadilla.core.task_definitions import (
    AsyncTaskDefinition,
    SyncTaskDefinition,
    TaskDefinition,
)
from quesadilla.core.task_executables import (
    AsyncTaskExecutable,
    Failure,
    Success,
    SyncTaskExecutable,
)
from quesadilla.core.task_metadata import BaseTaskMetadata, TaskExecutionContext
from quesadilla.core.task_queues import GenericQueuedTask, TaskQueue


@dataclass(frozen=True)
class Task[**P, T]:
    task_definition: TaskDefinition[P, T]

    @cached_property
    def task_queue(self) -> TaskQueue:
        return self.task_definition.task_queue

    def upgrade(self, queued_task: GenericQueuedTask) -> QueuedTask[P, T]:
        return QueuedTask.from_generic(queued_task, self)

    def queue(self, *args: P.args, **kwargs: P.kwargs) -> QueuedTask[P, T]:
        task_execution_context = TaskExecutionContext(args=tuple(args), kwargs=kwargs)
        queued_task = QueuedTask(task=self, execution_context=task_execution_context)

        self.task_queue.queue(queued_task.generic)

        return queued_task

    async def aqueue(self, *args: P.args, **kwargs: P.kwargs) -> QueuedTask[P, T]:
        task_execution_context = TaskExecutionContext(args=tuple(args), kwargs=kwargs)
        queued_task = QueuedTask(task=self, execution_context=task_execution_context)

        await self.task_queue.aqueue(queued_task.generic)

        return queued_task

    def find(self, task_id: ulid.ULID) -> QueuedTask[P, T] | None:
        queued_task: QueuedTask[P, T] | None = (
            QueuedTask.from_generic(generic_queued_task, self)
            if (generic_queued_task := self.task_queue.find(task_id))
            else None
        )
        return queued_task

    async def afind(self, task_id: ulid.ULID) -> QueuedTask[P, T] | None:
        queued_task: QueuedTask[P, T] | None = (
            QueuedTask.from_generic(generic_queued_task, self)
            if (generic_queued_task := await self.task_queue.afind(task_id))
            else None
        )
        return queued_task


@dataclass(frozen=True)
class SyncTask[**P, T](Task[P, T]):
    task_definition: SyncTaskDefinition[P, T]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.task_definition(*args, **kwargs)


def sync_task[
    **P, T
](
    task_queue: TaskQueue,
    *,
    name: str | None = None,
) -> Callable[
    [Callable[P, T]], SyncTask[P, T]
]:
    def wrapper(f: Callable[P, T]) -> SyncTask[P, T]:
        task_executable = SyncTaskExecutable(name or f.__name__, f)
        task_queue.register_task_executable(task_executable)
        return SyncTask(SyncTaskDefinition(task_queue, task_executable))

    return wrapper


@dataclass(frozen=True)
class AsyncTask[**P, T](Task[P, T]):
    task_definition: AsyncTaskDefinition[P, T]

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self.task_definition(*args, **kwargs)


def async_task[
    **P, T
](
    task_queue: TaskQueue,
    *,
    name: str | None = None,
) -> Callable[
    [Callable[P, Awaitable[T]]], AsyncTask[P, T]
]:
    def wrapper(f: Callable[P, Awaitable[T]]) -> AsyncTask[P, T]:
        task_executable = AsyncTaskExecutable(name or f.__name__, f)
        task_queue.register_task_executable(task_executable)
        return AsyncTask(AsyncTaskDefinition(task_queue, task_executable))

    return wrapper


@dataclass(frozen=True)
class QueuedTask[**P, T](BaseTaskMetadata[T]):
    task: Task[P, T] = field(kw_only=True)

    @cached_property
    def generic(self) -> GenericQueuedTask:
        return GenericQueuedTask(
            id=self.id,
            task_queue=self.task.task_definition.task_queue,
            task_executable=self.task.task_definition.task_executable,
            execution_context=self.execution_context,
            execution_result=self.execution_result,
            queued_at=self.queued_at,
            started_at=self.started_at,
            finished_at=self.finished_at,
        )

    @staticmethod
    def from_generic[
        **NP, NT
    ](queued_task: GenericQueuedTask, task: Task[NP, NT]) -> QueuedTask[NP, NT]:
        return QueuedTask(
            id=queued_task.id,
            execution_context=queued_task.execution_context,
            execution_result=queued_task.execution_result,
            queued_at=queued_task.queued_at,
            started_at=queued_task.started_at,
            finished_at=queued_task.finished_at,
            task=task,
        )

    @cached_property
    def result(self) -> Success[Any] | Failure:
        if not self.execution_result.finished:
            raise TaskNotFinishedError(
                namespace=self.task.task_queue.namespace,
                task_queue_name=self.task.task_queue.name,
                task_name=self.task.task_definition.name,
                task_id=self.id,
            )

        if self.execution_result.exc is not None:
            return Failure(self.execution_result.exc)
        return Success(self.execution_result.value)

    def refresh(self) -> QueuedTask[P, T]:
        if (queued_task := self.task.find(self.id)) is None:
            raise TaskDoesNotExistAnymoreError(
                namespace=self.task.task_queue.namespace,
                task_queue_name=self.task.task_queue.name,
                task_name=self.task.task_definition.name,
                task_id=self.id,
            )
        return queued_task

    async def arefresh(self) -> QueuedTask[P, T]:
        if (queued_task := await self.task.afind(self.id)) is None:
            raise TaskDoesNotExistAnymoreError(
                namespace=self.task.task_queue.namespace,
                task_queue_name=self.task.task_queue.name,
                task_name=self.task.task_definition.name,
                task_id=self.id,
            )
        return queued_task

    def wait_for(self, interval: float = 0.1) -> QueuedTask[P, T]:
        while not (cursor := self.refresh()).finished:
            time.sleep(interval)
        return cursor

    async def await_for(self, interval: float = 0.1) -> QueuedTask[P, T]:
        while not (cursor := await self.arefresh()).finished:
            await asyncio.sleep(interval)
        return cursor
