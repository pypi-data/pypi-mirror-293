import typer, os
from typing import Optional


### ENV_KEY ###
TMA_PREFIX = "TMA_PREFIX"


true_set = set(["y", "yes", "Y", "YES", "Yes"])
false_set = set(["n", "no", "N", "NO", "No"])


app = typer.Typer()


@app.command(name="des")
def description():
    des_string = f"""
tma_flutter make new module name("prefix" + "_" + "input module name").
new module name should be unique include external library(pub.dev).
new module name used for creating local package and app.

you can set prefix in bash typing
$ export {TMA_PREFIX}="[your prefix]"

you don't want to use prefix module name, then
use "--no-prefix" option or just set empty value like
$ export {TMA_PREFIX}=""
"""
    print(des_string)


def make_new_module_name(module_name: str) -> Optional[str]:
    new_module_name = prefix_module_name(module_name)

    if module_name == new_module_name:
        print(
            """
module prefix name has not been set.
Please read description typing
$ tma_flutter prefix des
"""
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
        print(
            """           
you can read prefix description and how to set typing
$ tma_flutter prefix des
"""
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
    prefix = os.getenv(TMA_PREFIX)
    if prefix != None:
        prefix = prefix.strip()
    return module_name if not prefix else prefix + "_" + module_name
