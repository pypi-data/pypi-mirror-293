import typer
from rich import print
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import IntPrompt, Prompt

from perika.clock import LevelTimer
from perika.game.choises import LevelComplexity
from perika.game.player import Player
from perika.game.rule import Game
from perika.game.text import PlayerAnswer


def start_game() -> None:
    name = Prompt.ask(
        prompt="Enter your name :waving_hand:",
        default="Guest",
        show_default=False,
    )

    print(f"Hello [green]{name}![/green]")

    lvl_hard = Prompt.ask(
        prompt="Enter level hard :flexed_biceps:",
        choices=LevelComplexity.list_keys(),
        default=LevelComplexity.easy.name,
        show_choices=True,
    )

    lvl_size = IntPrompt.ask("Enter level size (int, max: 10) :sunglasses:", default=1, show_default=False)

    player = Player(name)

    engine_name = Prompt.ask(
        "Set text engine :brain:",
        default="fishtext",
        choices=["fishtext", "gigachat"],
        show_choices=True,
    )

    game_rule = Game(lvl_hard, lvl_size, player, engine_name)  # type: ignore

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Generate level...", total=None)
        game_level = game_rule.generate_level()

    print(
        Panel(
            f"Game information! :flag_in_hole: \n\n "
            f"Player name: [red]{name}[/red] \n "
            f"Level hard: [yellow]{lvl_hard.capitalize()} [/yellow]\n "
            f"Level size: [green]{lvl_size}[/green]\n "
            f"Text generating engine: [blue]{engine_name.capitalize()}[/blue]",
            title="Game level info",
        ),
    )

    start_game = typer.confirm("Start the game?", default=True, show_default=True)

    if not start_game:
        msg = "Bye-bye .. game cancelled :("
        raise typer.Abort(msg)

    cnt = 1
    for task in game_level:
        print(Panel.fit(task(), title=f"Round {cnt}"))
        with LevelTimer() as timer:
            answer = PlayerAnswer(Prompt.ask("[bold red] your prompt -> "))

        print(timer.result(task.compare(answer)))
        cnt += 1
