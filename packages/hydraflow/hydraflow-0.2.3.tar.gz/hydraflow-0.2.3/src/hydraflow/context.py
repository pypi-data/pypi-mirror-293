"""
This module provides context managers to log parameters and manage the MLflow
run context.
"""

from __future__ import annotations

import logging
import os
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import mlflow
from hydra.core.hydra_config import HydraConfig
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from hydraflow.mlflow import get_artifact_dir, log_params

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from mlflow.entities.run import Run

log = logging.getLogger(__name__)


@dataclass
class Info:
    output_dir: Path
    artifact_dir: Path


@contextmanager
def log_run(
    config: object,
    *,
    synchronous: bool | None = None,
) -> Iterator[Info]:
    """
    Log the parameters from the given configuration object and manage the MLflow
    run context.

    This context manager logs the parameters from the provided configuration object
    using MLflow. It also manages the MLflow run context, ensuring that artifacts
    are logged and the run is properly closed.

    Args:
        config: The configuration object to log the parameters from.
        synchronous: Whether to log the parameters synchronously.
            Defaults to None.

    Yields:
        Info: An `Info` object containing the output directory and artifact directory
        paths.

    Example:
        with log_run(config) as info:
            # Perform operations within the MLflow run context
            pass
    """
    log_params(config, synchronous=synchronous)

    hc = HydraConfig.get()
    output_dir = Path(hc.runtime.output_dir)
    info = Info(output_dir, get_artifact_dir())

    # Save '.hydra' config directory first.
    output_subdir = output_dir / (hc.output_subdir or "")
    mlflow.log_artifacts(output_subdir.as_posix(), hc.output_subdir)

    def log_artifact(path: Path) -> None:
        local_path = (output_dir / path).as_posix()
        mlflow.log_artifact(local_path)

    try:
        with watch(log_artifact, output_dir):
            yield info

    except Exception as e:
        log.error(f"Error during log_run: {e}")
        raise

    finally:
        # Save output_dir including '.hydra' config directory.
        mlflow.log_artifacts(output_dir.as_posix())


@contextmanager
def watch(
    func: Callable[[Path], None],
    dir: Path | str = "",
    timeout: int = 60,
) -> Iterator[None]:
    """
    Watch the given directory for changes and call the provided function
    when a change is detected.

    This context manager sets up a file system watcher on the specified directory.
    When a file modification is detected, the provided function is called with
    the path of the modified file. The watcher runs for the specified timeout
    period or until the context is exited.

    Args:
        func: The function to call when a change is
            detected. It should accept a single argument of type `Path`,
            which is the path of the modified file.
        dir: The directory to watch. If not specified,
            the current MLflow artifact URI is used. Defaults to "".
        timeout: The timeout period in seconds for the watcher
            to run after the context is exited. Defaults to 60.

    Yields:
        None

    Example:
        with watch(log_artifact, "/path/to/dir"):
            # Perform operations while watching the directory for changes
            pass
    """
    dir = dir or get_artifact_dir()

    handler = Handler(func)
    observer = Observer()
    observer.schedule(handler, dir, recursive=True)
    observer.start()

    try:
        yield

    except Exception as e:
        log.error(f"Error during watch: {e}")
        raise

    finally:
        elapsed = 0
        while not observer.event_queue.empty():
            time.sleep(0.2)
            elapsed += 0.2
            if elapsed > timeout:
                break

        observer.stop()
        observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, func: Callable[[Path], None]) -> None:
        self.func = func

    def on_modified(self, event: FileModifiedEvent) -> None:
        file = Path(event.src_path)
        if file.is_file():
            self.func(file)


@contextmanager
def chdir_artifact(
    run: Run,
    artifact_path: str | None = None,
) -> Iterator[Path]:
    """
    Change the current working directory to the artifact directory of the
    given run.

    This context manager changes the current working directory to the artifact
    directory of the given run. It ensures that the directory is changed back
    to the original directory after the context is exited.

    Args:
        run: The run to get the artifact directory from.
        artifact_path: The artifact path.
    """
    curdir = Path.cwd()
    path = mlflow.artifacts.download_artifacts(
        run_id=run.info.run_id,
        artifact_path=artifact_path,
    )

    os.chdir(path)
    try:
        yield Path(path)

    finally:
        os.chdir(curdir)
