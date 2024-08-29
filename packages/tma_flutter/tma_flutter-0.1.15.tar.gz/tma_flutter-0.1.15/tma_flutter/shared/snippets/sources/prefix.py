from typing import Optional
from tma_flutter.shared.env.sources import env
from tma_flutter.shared.snippets.sources import echo


true_set = set(["y", "yes", "Y", "YES", "Yes"])
false_set = set(["n", "no", "N", "NO", "No"])


def make_new_module_name(module_name: str) -> Optional[str]:
    new_module_name = prefix_module_name(module_name)

    if module_name == new_module_name:
        echo.command(
            description="""module prefix name has not been set.
Please read description typing""",
            command="$ tma_flutter env prefix",
        )

    print(
        f"""your new module name is {new_module_name}.
new module name used for creating local package and app.
Is it ok to continue ? [y/n]""",
        end=" ",
    )
    check = input_check()
    print()
    if check:
        return new_module_name
    else:
        echo.command(
            description="you can read prefix description and how to set typing",
            command="$ tma_flutter env prefix",
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
            f"""Invalid typing error : [magenta]{check}[/magenta]
If you are positive,
Please type [magenta]{true_set}[/magenta].
Or not,
Please type [magenta]{false_set}[/magenta]."""
        )


def prefix_module_name(module_name: str) -> str:
    prefix = env.get_value(env.ENV_KEY.prefix)
    return module_name if not prefix else prefix + "_" + module_name
