from __future__ import annotations

from enum import Enum, unique


@unique
class LevelComplexity(Enum):
    easy = 1
    medium = 2
    hard = 3

    @classmethod
    def list_keys(cls) -> list[str]:
        return [x.name for x in cls]

    @classmethod
    def list_value(cls) -> list[int]:
        return [x.value for x in cls]
