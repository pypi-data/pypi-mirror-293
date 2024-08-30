from __future__ import annotations

from typing import TYPE_CHECKING

from perika.engine.fishtext import FishTextEngine
from perika.game.choises import LevelComplexity
from perika.game.level import Level
from perika.game.task import Task

if TYPE_CHECKING:
    from perika.engine.base import TextEngine
    from perika.game.player import Player


class Game:
    def __init__(
        self,
        level_hard: LevelComplexity,
        level_size: int,
        player: Player,
        engine_name: str,
    ) -> None:
        self.level_hard = level_hard
        self.level_size = level_size
        self.player = player
        self.engine = self._resolve_engine(engine_name)

    def _resolve_engine(self, eng: str) -> TextEngine:
        if eng == "fishtext":
            return FishTextEngine(complexity=LevelComplexity[self.level_hard].value)  # type: ignore
        msg = "Engine not implemented"
        raise NotImplementedError(msg)

    def generate_level(self) -> Level:
        result = [Task(self.engine.get_or_generate()) for _ in range(self.level_size)]
        return Level(result)
