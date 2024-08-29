import typer
from typing import Optional
from tma_flutter.shared.env.sources import env
from tma_flutter.shared.snippets.sources import echo


true_set = set(["y", "yes", "Y", "YES", "Yes"])
false_set = set(["n", "no", "N", "NO", "No"])


app = typer.Typer()


@app.command(name="des")
def description():
    print(
        """
tma_flutter make new module name("prefix" + "_" + "input module name").
new module name should be unique include external library(pub.dev).
new module name used for creating local package and app.
"""
    )

    echo.command(
        description="you can set prefix typing",
        command="$ tma_flutter env update prefix [your prefix]",
    )

    echo.command(
        description="""
you don't want to use prefix module name,
then use "--no-prefix" option
""",
        command="$ tma_flutter [presentation/domain] --no-prefix [your module name]",
    )

    echo.command(
        description="or just set empty value like",
        command='''$ tma_flutter env update prefix ""''',
    )

    echo.command(
        description="or use env delete option like",
        command="$ tma_flutter env delete prefix",
    )


def make_new_module_name(module_name: str) -> Optional[str]:
    new_module_name = prefix_module_name(module_name)

    if module_name == new_module_name:
        echo.command(
            description="""
module prefix name has not been set.
Please read description typing
""",
            command="$ tma_flutter prefix des",
        )

    print(
        f"""
your new module name is {new_module_name}.
new module name used for creating local package and app.
Is it ok to continue ? [y/n]
"""
    )
    check = input_check()
    if check:
        return new_module_name
    else:
        echo.command(
            description="you can read prefix description and how to set typing",
            command="$ tma_flutter prefix des",
        )
        return None


def input_check() -> bool:
    while True:
        check = input().strip()
        if check in true_set:
            return True
        elif check in false_set:
            return False
        print(
            f"""
Invalid typing error : {check}
If you are positive,
Please type {true_set}.
Or not,
Please type {false_set}.
"""
        )


def prefix_module_name(module_name: str) -> str:
    prefix = env.get_value(env.ENV_KEY.prefix)
    return module_name if not prefix else prefix + "_" + module_name
