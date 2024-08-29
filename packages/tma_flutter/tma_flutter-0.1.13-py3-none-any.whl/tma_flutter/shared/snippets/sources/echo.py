import typer
from typing import Optional


def command(
    command: str,
    description: Optional[str] = None,
):
    if description:
        print(description, end="")
    typer.secho(
        command,
        fg=typer.colors.MAGENTA,
    )
