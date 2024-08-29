import typer
from tma_flutter.modules.layers.sources import presentation, domain
from tma_flutter.melos.sources import melos
from tma_flutter.shared.env.sources import env_typer


app = typer.Typer()
app.add_typer(presentation.app, name="presentation")
app.add_typer(domain.app, name="domain")
app.add_typer(melos.app, name="melos")
app.add_typer(env_typer.app, name="env")


if __name__ == "__main__":
    app()
