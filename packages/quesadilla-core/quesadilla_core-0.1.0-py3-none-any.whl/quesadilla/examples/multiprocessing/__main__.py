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

import asyncio
import logging
import multiprocessing
import random
import signal
import time
from collections.abc import Callable, Coroutine
from types import FrameType
from typing import Any

from quesadilla import TaskQueues, async_task, sync_task
from quesadilla.connectors.in_memory import ProcessSafeInMemoryConnector
from quesadilla.runners import MultiprocessingRunner, RoundRobinSelector, RunnerConfig

# configure logging


logging.basicConfig(
    format="{asctime} | {name} | {levelname} | {message}", style="{", level=logging.INFO
)
logger = logging.getLogger(__name__)


# define the task queue


queues = TaskQueues("quesadilla", connector=ProcessSafeInMemoryConnector())

default_queue = queues.new("default")


# define some simple tasks


@sync_task(default_queue)
def simple_sync_task(i: int) -> bool:
    return i == 0


@async_task(default_queue)
async def simple_async_task(i: int) -> bool:
    return i == 0


@sync_task(default_queue)
def sometimes_exception_task(i: int) -> bool:
    if random.random() < 0.01:
        raise Exception("(Un)lucky 1%!")
    return i == 0


# helper method for running coroutines in an asyncio runner


def run_coro[**P, T](coro: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return asyncio.run(coro(*args, **kwargs))

    return wrapper


# configure the runner


runner = MultiprocessingRunner(
    default_queue,
    config=RunnerConfig(
        brokers=2,
        workers=3,
        worker_selector_class=RoundRobinSelector,
    ),
)


# main loop


if __name__ == "__main__":
    logger.info("Main thread starting...")

    # we will schedule tasks whichever way we can to test all possible combinations
    def schedule_some_tasks() -> None:
        choices = [
            simple_sync_task.queue,
            simple_async_task.queue,
            sometimes_exception_task.queue,
            run_coro(simple_sync_task.aqueue),
            run_coro(simple_async_task.aqueue),
            run_coro(sometimes_exception_task.aqueue),
        ]
        for _ in range(random.randint(3, 10)):
            random.choice(choices)(random.randint(0, 1))

    stopped = multiprocessing.get_context("spawn").Event()

    def shutdown(sig: int | None = None, frame: FrameType | None = None) -> None:
        if not stopped.is_set():
            s = signal.Signals(sig) if sig is not None else sig
            if s is not None:
                logger.warning(f"Received signal {s.name}")
            if s in frozenset((signal.SIGTERM, signal.SIGINT)):
                logger.info("Main thread stopping...")
                stopped.set()
                runner.signal(sig)

    # run the runner in the background as a context manager inline
    with runner:
        # attach the stop signals after we fork
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        # run the main loop
        # schedules tasks on the queue indefinitely while the runner is running
        while not stopped.is_set():
            schedule_some_tasks()
            time.sleep(random.random() * 5)

    logger.info("Main thread exited gracefully")
