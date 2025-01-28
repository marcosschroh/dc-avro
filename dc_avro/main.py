import ast
from typing import Dict, List, Optional, Sequence

import rich
import typer
from dataclasses_avroschema import (
    ModelGenerator,
    ModelType,
    serialization,
)

from . import _schema_utils
from ._diff import DiffTypes, context_diff, table_diff, unified_diff
from ._types import JsonDict, SerializationType
from .exceptions import InvalidSchema, JsonRequired

app = typer.Typer()
console = rich.console.Console()


def generate_error_messages(
    path_name: Optional[str] = "--path", url_name: Optional[str] = "--url"
) -> Dict[str, str]:
    return {
        "all_specified": f"You can not specify both {path_name} and {url_name}",
        "required": f"{path_name} or {url_name} must be specified",
    }


def get_resource(
    *,
    path: Optional[str] = None,
    url: Optional[str] = None,
    error_messages: Optional[Dict[str, str]] = None,
) -> JsonDict:
    error_messages = error_messages or generate_error_messages()

    if all([path, url]):
        raise typer.BadParameter(error_messages["all_specified"])
    elif path is not None:
        return _schema_utils.get_resource_from_path(path=path)
    elif url is not None:
        return _schema_utils.get_resource_from_url(url=url)
    else:
        raise typer.BadParameter(error_messages["required"])


def get_raw_resource(
    *,
    path: Optional[str] = None,
    url: Optional[str] = None,
    error_messages: Optional[Dict[str, str]] = None,
) -> Sequence[str]:
    error_messages = error_messages or generate_error_messages()

    if all([path, url]):
        raise typer.BadParameter(error_messages["all_specified"])
    elif path is not None:
        return _schema_utils.get_raw_resource_from_path(path=path)
    elif url is not None:
        return _schema_utils.get_raw_resource_from_url(url=url)
    else:
        raise typer.BadParameter(error_messages["required"])


@app.command()
def generate_model(
    path: str = typer.Option(None),
    url: str = typer.Option(None),
    model_type: ModelType = typer.Option(
        ModelType.DATACLASS,
        help="Model Type",
    ),
):
    resource = get_resource(path=path, url=url)
    _schema_utils.validate(schema=resource)

    model_generator = ModelGenerator()
    result = model_generator.render(schema=resource, model_type=model_type.value)

    print(result)


@app.command()
def schema_diff(
    source_path: str = typer.Option(None, help="Source path to the local schema"),
    source_url: str = typer.Option(None, help="Source schema url"),
    target_path: str = typer.Option(None, help="Target path to the local schema"),
    target_url: str = typer.Option(None, help="Target schema url"),
    only_deltas: bool = typer.Option(
        help=(
            "Whether to include only deltas. If set to True then only deltas are "
            "included rather than the whole resource in the diff result. "
            "Default to False."
        ),
        default=False,
    ),
    num_lines: int = typer.Option(
        5, help="Number of lines to show in the diff when context is set to True"
    ),
    type: DiffTypes = typer.Option(
        "table", help="Type of diff to display: table, context or unified"
    ),
) -> None:
    source_resource = get_raw_resource(
        path=source_path,
        url=source_url,
        error_messages=generate_error_messages(
            path_name="--source-path", url_name="--source-url"
        ),
    )

    target_resource = get_raw_resource(
        path=target_path,
        url=target_url,
        error_messages=generate_error_messages(
            path_name="--target-path", url_name="--target-url"
        ),
    )

    if type == DiffTypes.TABLE:
        console.print(
            table_diff(
                source_resource=source_resource,
                source_name=source_path or source_url,
                target_resource=target_resource,
                target_name=target_path or target_url,
                only_deltas=only_deltas,
                num_lines=num_lines,
            )
        )
    elif type == DiffTypes.CONTEXT:
        console.print(
            context_diff(
                source_resource=source_resource,
                source_name=source_path or source_url,
                target_resource=target_resource,
                target_name=target_path or target_url,
                only_deltas=only_deltas,
                num_lines=num_lines,
            )
        )
    else:
        console.print(
            unified_diff(
                source_resource=source_resource,
                source_name=source_path or source_url,
                target_resource=target_resource,
                target_name=target_path or target_url,
                only_deltas=only_deltas,
                num_lines=num_lines,
            )
        )


@app.command()
def serialize(
    data: str = typer.Argument(None, callback=ast.literal_eval),
    path: str = typer.Option(None),
    url: str = typer.Option(None),
    serialization_type: SerializationType = typer.Option(
        SerializationType.AVRO,
    ),
) -> None:
    resource = get_resource(path=path, url=url)
    _schema_utils.validate(schema=resource)

    output = serialization.serialize(
        data,  # type: ignore
        resource,
        serialization_type=serialization_type,  # type: ignore
    )
    console.print(output)


@app.command()
def deserialize(
    event: str,
    path: str = typer.Option(None),
    url: str = typer.Option(None),
    serialization_type: SerializationType = typer.Option(
        SerializationType.AVRO,
    ),
) -> None:
    resource = get_resource(path=path, url=url)
    _schema_utils.validate(schema=resource)

    data = (
        ast.literal_eval(event)
        if serialization_type == SerializationType.AVRO.value
        else event.encode()
    )

    output = serialization.deserialize(
        data=data,
        schema=resource,
        serialization_type=serialization_type,  # type: ignore
    )
    console.print(output)


@app.command()
def validate_schema(
    path: Optional[str] = typer.Option(None, help="Path to the local schema"),
    url: Optional[str] = typer.Option(None, help="Schema url"),
) -> None:
    resource = get_resource(path=path, url=url)

    if _schema_utils.validate(schema=resource):
        console.print("[bold green]Valid schema!![/bold green] :+1: \n")
        console.print(resource)


@app.command()
def lint(files: List[str]) -> None:
    errors: dict = {}
    valid_schemas = []
    for path in files:
        try:
            schema = _schema_utils.get_resource_from_path(path=path)
        except JsonRequired as e:
            errors[path] = e
            continue
        try:
            _schema_utils.validate(schema=schema)
        except InvalidSchema as e:
            errors[path] = e
            continue
        valid_schemas.append(path)
    if valid_schemas:
        console.print(f"\n:+1: Total valid schemas: {len(valid_schemas)}")
        for valid in valid_schemas:
            console.print(valid)
    if errors:
        error_msg = f"Total errors detected: {len(errors.keys())}"
        for error_path, error in errors.items():
            console.print(":boom: File: " + error_path)
            console.print(f"[red]{error}[/red]")
        app.pretty_exceptions_show_locals = False
        raise InvalidSchema(error_msg)


@app.command(help="Generate fake data for a given avsc schema")
def generate_data(
    resource: str = typer.Argument(None, help="Path or URL to the avro schema"),
    count: int = typer.Option(
        1, help="Number of data to generate, more than one prints a list"
    ),
) -> None:
    schema = _schema_utils.get_schema(resource=resource)
    data = _schema_utils.generate_data(schema=schema, count=count)
    console.print(data)
