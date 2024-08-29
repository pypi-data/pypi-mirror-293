import typer
from typing_extensions import Annotated
from tma_flutter.shared.snippets.sources import echo
from rich import print
from rich.console import Console
from rich.table import Table
from tma_flutter.shared.env.sources import env


complete_key_items = [
    (env.ENV_KEY.prefix, "prefix is used for make new module name"),
]

# def complete_key(incomplete: str):
#     completion = []
#     for name, help_text in complete_key_items:
#         name_str = name.value
#         if name_str.startswith(incomplete):
#             complete_item = (name, help_text)
#             completion.append(complete_item)
#     return completion


def complete_key(incomplete: str):
    for name, help_text in complete_key_items:
        name_str = name.value
        if name_str.startswith(incomplete):
            yield (name, help_text)


console = Console()


ANNOTATED_KEY = Annotated[
    env.ENV_KEY,
    typer.Option(
        help="Select env key",
        autocompletion=complete_key,
    ),
]


app = typer.Typer()


@app.command(name="update")
def update(
    key: ANNOTATED_KEY,
    value: Annotated[str, typer.Argument()],
):
    env_dict = env.read_yaml()
    key = key.value
    value = value.strip()
    to_update = {key: value}

    if env_dict == None:
        env.write_yaml(env_dict=to_update)
    else:
        env_dict.update(to_update)
        env.write_yaml(env_dict=env_dict)


@app.command(name="delete")
def delete(key: ANNOTATED_KEY):
    update(key, "")
    print(f"Complete Delete Key : [magenta]{key.value}[/magenta]")


@app.command(name="search")
def search(key: ANNOTATED_KEY):
    value = env.get_value(key)
    if not value:
        echo.command(
            description="""
Value has not been set.
You can set value typing
""",
            command="$ tma_flutter env update [key:{ENV_KEY}] [value]",
        )
    else:
        print(
            f"""
Key : [magenta]{key.value}[/magenta]
Value : [magenta]{value}[/magenta]
"""
        )


## search -all, -a
@app.command(name="search_all")
def search_all():
    table = Table("KEY", "VALUE")
    env_dict = env.read_yaml()
    for key in env.ENV_KEY:
        key = key.value
        value = env_dict.get(key, "") if env_dict != None else ""
        table.add_row(key, value)
    console.print(table)


if __name__ == "__main__":
    app()
