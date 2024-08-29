import functools
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Timer:
    timers: ClassVar[dict[str, float]] = dict()
    name: str | None = None
    text: str = "Elapsed time: {:0.4f} seconds\n"
    logger: Callable[..., None] | None = print
    _start_time: float | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        """Add timer to dict of timers after initialization"""
        if self.name is not None:
            self.timers.setdefault(self.name, 0)

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()

    def __call__(self, func):
        """Support using Timer as a decorator"""

        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper_timer

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise Exception("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise Exception("Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            # Instead of logger being a print, it can be used logging.info() or .write().
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time
