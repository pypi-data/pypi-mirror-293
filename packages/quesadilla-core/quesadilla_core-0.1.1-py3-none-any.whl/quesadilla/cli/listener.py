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

import enum
import logging
import multiprocessing
import signal
import threading
from types import FrameType
from typing import Annotated, TypedDict

import typer

from quesadilla.cli.utils import task_queue
from quesadilla.core.logging import TaskQueueLoggingExtras
from quesadilla.core.task_queues import TaskQueue
from quesadilla.runners import (
    MultiprocessingRunner,
    MultithreadingRunner,
    RandomSelector,
    RoundRobinSelector,
    RunnerConfig,
)


class Parallelism(enum.StrEnum):
    THREADS = enum.auto()
    PROCESSES = enum.auto()


class WorkerSelector(enum.StrEnum):
    ROUNDROBIN = enum.auto()
    RANDOM = enum.auto()


class ListenerLoggingExtras(TypedDict):
    task_queue: TaskQueueLoggingExtras
    parallelism: str
    brokers: int
    workers: int
    worker_selector: str


def listener(
    task_queue: Annotated[
        TaskQueue,
        typer.Argument(
            parser=task_queue,
            help=("Dotted path of the TaskQueue object <path.to.module::task_queue>"),
            show_default=False,
        ),
    ],
    parallelism: Annotated[
        Parallelism, typer.Option(help="Parallelization type")
    ] = Parallelism.THREADS,
    brokers: Annotated[int, typer.Option(help="Number of broker threads")] = 1,
    workers: Annotated[int, typer.Option(help="Number of worker threads")] = 1,
    worker_selector: Annotated[
        WorkerSelector, typer.Option(help="Worker selector implementation")
    ] = WorkerSelector.ROUNDROBIN,
) -> None:
    """
    Run a listener process for processing tasks
    """
    match worker_selector:
        case WorkerSelector.ROUNDROBIN:
            worker_selector_class = RoundRobinSelector
        case WorkerSelector.RANDOM:
            worker_selector_class = RandomSelector

    runner_config = RunnerConfig(
        brokers=brokers,
        workers=workers,
        worker_selector_class=worker_selector_class,
    )

    match parallelism:
        case Parallelism.THREADS:
            stopped = threading.Event()
            runner = MultithreadingRunner(task_queue, config=runner_config)
        case Parallelism.PROCESSES:
            stopped = multiprocessing.get_context("spawn").Event()
            runner = MultiprocessingRunner(task_queue, config=runner_config)

    logger = logging.getLogger(__name__)
    logging_extras: ListenerLoggingExtras = {
        "task_queue": task_queue.logging_extras,
        "parallelism": parallelism.value,
        "brokers": brokers,
        "workers": workers,
        "worker_selector": worker_selector.value,
    }

    def shutdown(sig: int | None = None, frame: FrameType | None = None) -> None:
        if not stopped.is_set():
            s = signal.Signals(sig) if sig is not None else sig
            if s is not None:
                logger.warning(f"Received signal {s.name}", extra=logging_extras)
            if s in frozenset((signal.SIGTERM, signal.SIGINT)):
                logger.info("Listener stopping...", extra=logging_extras)
                stopped.set()
                runner.signal(sig)

    logger.info("Listener starting...", extra=logging_extras)

    with runner:
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)
        runner.wait()

    logger.info("Listener exited gracefully", extra=logging_extras)
