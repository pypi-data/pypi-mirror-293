import typer
from typing import Optional


def command(
    command: str,
    description: Optional[str] = None,
):
    if description:
        print(description)
    typer.secho(
        command,
        fg=typer.colors.MAGENTA,
    )
    print()
