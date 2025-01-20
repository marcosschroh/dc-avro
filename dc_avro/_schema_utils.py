import json
from typing import Any, Iterable
from urllib.parse import urlparse

import httpx
from fastavro import _schema_common, parse_schema
from fastavro.types import Schema
from fastavro.utils import generate_many, generate_one

from ._types import JsonDict
from .exceptions import InvalidSchema, JsonRequired


def get_resource_from_url(url: str) -> JsonDict:
    try:
        response = httpx.get(url)
        return response.json()
    except json.JSONDecodeError as exc:
        raise JsonRequired(f"Can not convert to json the resource from {url}") from exc


def get_resource_from_path(path: str) -> JsonDict:
    with open(path, mode="r") as resource:
        schema = resource.read()
        try:
            return json.loads(schema)
        except json.JSONDecodeError as exc:
            raise JsonRequired(
                f"Can not convert to json the resource from {path}"
            ) from exc


def get_raw_resource_from_url(url: str) -> list[str]:
    response = httpx.get(url)
    return [line for line in response.iter_lines()]


def get_raw_resource_from_path(path: str) -> list[str]:
    with open(path, mode="r") as resource:
        schema = resource.readlines()

    return schema


def validate(*, schema: JsonDict) -> bool:
    try:
        parse_schema(schema=schema)
        return True
    except _schema_common.SchemaParseException as exc:
        raise InvalidSchema(
            f"Schema {schema} is not valid.\n Error: `{str(exc)}`"
        ) from exc
    except _schema_common.UnknownType as exc:
        raise InvalidSchema(
            f"Schema {schema} is an unknown type.\n "
            "Make sure that its type is a python dictionary"
        ) from exc


def is_url(resource: str) -> bool:
    return urlparse(resource).scheme in (
        "http",
        "https",
    )


def get_schema(resource: str) -> Schema:
    """Get a schema from a uri or path."""
    if is_url(resource):
        return parse_schema(get_resource_from_url(resource))
    return parse_schema(get_resource_from_path(resource))


def generate_data(schema: Schema, count: int = 1) -> Iterable[Any]:
    """Generate data from a schema."""
    if count == 1:
        return generate_one(schema)
    return list(generate_many(schema, count=count))
