import typer

from perika.flow import start_game

app = typer.Typer()


@app.command("start")
def start() -> None:
    return start_game()
