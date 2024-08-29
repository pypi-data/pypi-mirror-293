import typer, os
from pathlib import Path
from typing import Optional, List
from typing_extensions import Annotated
from tma_flutter.modules.targets.interface.sources import interface
from tma_flutter.modules.targets.test.sources import test
from tma_flutter.modules.targets.view.sources import view
from tma_flutter.modules.targets.example.sources import example
from tma_flutter.modules.targets.feature.sources import feature
from tma_flutter.shared.snippets.sources import prefix


app = typer.Typer()


@app.command(name="make")
def make_module(
    module_name: Annotated[str, typer.Argument()],
    dependency_names: Annotated[Optional[List[str]], typer.Option("-dp")] = None,
):
    if not module_name.strip():
        print("Please input module name without spacing")
        return

    new_module_name = prefix.make_new_module_name(module_name)
    if new_module_name == None:
        return

    current_path = Path(os.getcwd())
    module_path = current_path.joinpath(module_name)
    Path(module_path).mkdir(parents=True, exist_ok=True)
    os.chdir(module_path)

    example_name = example.name(new_module_name)
    view_name = view.name(new_module_name)
    feature_name = feature.presentation_name(new_module_name)
    test_name = test.name(new_module_name)
    interface_name = interface.name(new_module_name)

    example.make_target(example_name)
    view.make_target(view_name)
    feature.make_target(feature_name)
    test.make_target(test_name)
    interface.make_target(interface_name)

    example.copy_template(
        example_name=example_name,
        view_name=view_name,
    )
    view.copy_template(
        view_name=view_name,
        feature_name=feature_name,
    )
    feature.copy_template(
        feature_name=feature_name,
        interface_name=interface_name,
    )
    test.copy_template(
        feature_name=feature_name,
    )
    interface.copy_template(
        interface_name=interface_name,
    )

    example.add_dependency(
        view_name=view_name,
    )
    view.add_dependency(
        feature_name=feature_name,
    )
    feature.add_dependency(
        interface_name=interface_name,
    )
    test.add_dependency_presentation(
        view_name=view_name,
        interface_name=interface_name,
    )
    if dependency_names:
        interface.add_dependency(dependency_names)


if __name__ == "__main__":
    app()
