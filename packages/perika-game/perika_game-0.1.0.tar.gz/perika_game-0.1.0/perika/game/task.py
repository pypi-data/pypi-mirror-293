import difflib
from dataclasses import dataclass
from typing import Optional

from perika.game.text import PlayerAnswer, TaskText


@dataclass
class TaskResult:
    equal: bool
    diff: Optional[str]

    def __repr__(self) -> str:
        return f"TaskResult \n equal >>> {self.equal}\n diff  >>> \n {self.diff}"


class Task:
    def __init__(self, text: TaskText) -> None:
        self.text = text

    def __call__(self) -> str:
        return self.text()

    def compare(self, player_input: PlayerAnswer) -> TaskResult:
        eq = self.text() == player_input()
        diff = "Success"
        if not eq:
            differ = difflib.Differ()
            raw_diff = list(differ.compare([self.text()], [player_input()]))
            diff = "\n".join(raw_diff)
        return TaskResult(equal=eq, diff=diff)
