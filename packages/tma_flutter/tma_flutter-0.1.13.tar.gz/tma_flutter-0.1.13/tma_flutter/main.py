import typer
from tma_flutter.modules.layers.sources import presentation, domain
from tma_flutter.melos.sources import melos
from tma_flutter.shared.env.sources import env_typer


app = typer.Typer()
app.add_typer(presentation.app, name="presentation")
app.add_typer(domain.app, name="domain")
app.add_typer(melos.app, name="melos")
app.add_typer(env_typer.app, name="env")


from typing_extensions import Annotated

valid_completion_items = [
    ("Camila", "The reader of books."),
    ("Carlos", "The writer of scripts."),
    ("Sebastian", "The type hints guy."),
]


def complete_name(incomplete: str):
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)


@app.command()
def main(
    name: Annotated[
        str, typer.Option(help="The name to say hi to.", autocompletion=complete_name)
    ] = "World",
):
    print(f"Hello {name}")


if __name__ == "__main__":
    app()
