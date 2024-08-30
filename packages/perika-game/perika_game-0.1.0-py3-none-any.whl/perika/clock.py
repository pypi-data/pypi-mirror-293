import time
from dataclasses import dataclass

from typing_extensions import Self

from perika.game.task import TaskResult


@dataclass
class TaskResultWithTime:
    result: TaskResult
    time: float

    def __repr__(self) -> str:
        return str(self.result) + f"\n User prompt time: {self.time:.2f} sec"


class LevelTimer:
    def __init__(self, result_pattern: str = "{:.2f}") -> None:
        self.result_pattern: str = result_pattern

    def __enter__(self) -> Self:
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # noqa: ANN204, ANN001
        self.end_time: float = time.time() - self.start_time

    def result(self, result: TaskResult) -> TaskResultWithTime:
        return TaskResultWithTime(result=result, time=self.end_time)
