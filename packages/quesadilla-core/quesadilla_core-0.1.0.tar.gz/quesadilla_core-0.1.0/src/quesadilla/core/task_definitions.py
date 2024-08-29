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


from dataclasses import dataclass
from functools import cached_property

from quesadilla.core.task_executables import (
    AsyncTaskExecutable,
    SyncTaskExecutable,
    TaskExecutable,
)
from quesadilla.core.task_queues import TaskQueue


@dataclass(frozen=True)
class TaskDefinition[**P, T]:
    task_queue: TaskQueue
    task_executable: TaskExecutable[P, T]

    @cached_property
    def name(self) -> str:
        return self.task_executable.name


@dataclass(frozen=True)
class SyncTaskDefinition[**P, T](TaskDefinition[P, T]):
    task_executable: SyncTaskExecutable[P, T]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.task_executable(*args, **kwargs)


@dataclass(frozen=True)
class AsyncTaskDefinition[**P, T](TaskDefinition[P, T]):
    task_executable: AsyncTaskExecutable[P, T]

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self.task_executable(*args, **kwargs)
