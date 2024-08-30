#!/usr/bin/env python3

from jinja2 import Template
import os
from pathlib import Path
import shutil
import tomllib
import typer
from typing_extensions import Annotated


app = typer.Typer()


def copy_directory(input_directory_path: Path, output_directory_path: Path):
    """
    Copy the contents of one directory to another directory.

    Parameters
    ----------
    input_directory_path : Path
        The path to the directory to be copied.
    output_directory_path : Path
        The path to the destination directory.

    Returns
    -------
    None
    """
    # Ensure the output directory exists, create it if it doesn't
    output_directory_path.mkdir(parents=True, exist_ok=True)

    # Copy the entire directory tree from input_directory_path to output_directory_path
    # dirs_exist_ok=True allows the copy to overwrite existing directories
    # copy_function=shutil.copy2 ensures that metadata (like timestamps) is also copied
    shutil.copytree(
        input_directory_path,
        output_directory_path,
        dirs_exist_ok=True,
        copy_function=shutil.copy2,
    )


@app.command()
def new(
    template_directory_path: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    project_config_path: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_directory_path: Path = Path("."),
):
    # Get the project configuration dictionary ################################

    with open(project_config_path, "rb") as file:
        config_dict = tomllib.load(file)

    # Create the output directory if it does not exist ########################

    copy_directory(template_directory_path, output_directory_path)

    # Walk the template directory #############################################

    for cur_dir, dirs, files in os.walk(output_directory_path, topdown=False):
        # cur_dir = path du répertoire courant dans l'exploration
        # dirs    = liste des répertoires dans "cur_dir"
        # files   = liste des fichiers dans "cur_dir"
        for name in files:
            template_file_path = os.path.join(cur_dir, name)
            print(template_file_path)
            if template_file_path.endswith(".j2"):
                # First render
                with open(template_file_path) as fd:
                    file_template = Template(fd.read())
                rendered_content = file_template.render(config_dict)

                # Second render (for nested templates)
                # TODO: is there a cleaner way to do nested rendering on variable content with Jinja2?
                # E.g. https://stackoverflow.com/questions/8862731/jinja-nested-rendering-on-variable-content
                # Alternative: faire un nested rendering sur le fichier de config seulement !
                file_template = Template(rendered_content)
                rendered_content = file_template.render(config_dict)

                # Write the rendered content to a new file
                new_file_path = template_file_path[:-3]

                with open(new_file_path, "w") as fd:
                    fd.write(rendered_content)

                os.remove(template_file_path)


@app.command()
def init():
    """
    Create a template of pyscaff.toml file in the current directory.
    """
    raise NotImplementedError("Not implemented yet")


if __name__ == "__main__":
    app()
