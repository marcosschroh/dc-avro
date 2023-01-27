from typing import Optional

import rich
import typer

from . import _schema_utils
from ._types import JsonDict

app = typer.Typer()
console = rich.console.Console()


def get_resource(*, path: Optional[str] = None, url: Optional[str] = None) -> JsonDict:
    if all([path, url]):
        raise typer.BadParameter("You can not specicy both --path and --url")
    elif path is not None:
        return _schema_utils.get_resource_from_path(path=path)
    elif url is not None:
        return _schema_utils.get_resource_from_url(url=url)
    else:
        raise typer.BadParameter("--path or --url must be specified")


@app.command()
def generate_model(
    path: str = typer.Option(None),
    url: str = typer.Option(None),
):
    print("Hello!!")


@app.command()
def generate_fake(
    path: str = typer.Option(None),
    url: str = typer.Option(None),
):
    print("Hello!!")


@app.command()
def schema_diff(source: str, target: str):
    print("Hello!!")


@app.command()
def serialize(
    path: str = typer.Option(None),
    url: str = typer.Option(None),
):
    print("Hello!!")


@app.command()
def validate_schema(
    path: str = typer.Option(None, help="Path to the local schema"),
    url: str = typer.Option(None, help="Schema url"),
):
    resource = get_resource(path=path, url=url)

    if _schema_utils.validate(schema=resource):
        console.print("[bold green]Valid schema!![/bold green] :+1: \n")
        console.print(resource)
