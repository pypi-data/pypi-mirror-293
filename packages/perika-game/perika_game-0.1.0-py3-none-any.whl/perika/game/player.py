from typing import NoReturn


class Player:
    def __init__(self, name: str) -> None:
        self.name = name

    def sync(self) -> NoReturn:
        raise NotImplementedError

    def metadata(self) -> NoReturn:
        raise NotImplementedError
