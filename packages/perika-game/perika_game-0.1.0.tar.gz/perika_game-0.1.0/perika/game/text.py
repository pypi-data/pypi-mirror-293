import functools


@functools.lru_cache
def _clean(text: str) -> str:
    return text.strip()


class TaskText:
    def __init__(self, text: str) -> None:
        self.text = text

    def __call__(self) -> str:
        return self.text


class PlayerAnswer:
    def __init__(self, player_text: str) -> None:
        self.player_text = player_text

    def __call__(self) -> str:
        return self.clean()

    def clean(self) -> str:
        self.player_text = _clean(self.player_text)
        return self.player_text
