from tma_flutter.shared.snippets.sources import echo


def prefix():
    print(
        """tma_flutter make new module name("prefix" + "_" + "input module name").
new module name should be unique include external library(pub.dev).
new module name used for creating local package and app."""
    )

    echo.command(
        description="you can set prefix typing",
        command="$ tma_flutter env update prefix [your prefix]",
    )

    echo.command(
        description="""you don't want to use prefix module name,
then use "--no-prefix" option""",
        command="$ tma_flutter [presentation/domain] make [your module name] --no-prefix",
    )

    echo.command(
        description="or just set empty value like",
        command='''$ tma_flutter env update prefix ""''',
    )

    echo.command(
        description="or use env delete option like",
        command="$ tma_flutter env delete prefix",
    )
