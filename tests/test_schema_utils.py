import json
import os
from unittest import mock

import pytest
from httpx import Response, codes

from dc_avro import JsonDict, exceptions
from dc_avro._schema_utils import (
    get_resource_from_path,
    get_resource_from_url,
    validate,
)


def test_get_resource_from_url(example_shema_json: JsonDict) -> None:
    url = "https://schema-registry/example.avsc"

    responnse = Response(status_code=codes.OK, json=example_shema_json)
    with mock.patch("dc_avro._schema_utils.httpx.get", return_value=responnse):
        assert get_resource_from_url(url)


def test_get_invalid_resource_from_url(invalid_resource) -> None:
    url = "https://schema-registry/example.avsc"

    responnse = Response(status_code=codes.OK, content=invalid_resource)
    with mock.patch("dc_avro._schema_utils.httpx.get", return_value=responnse):
        with pytest.raises(exceptions.JsonRequired) as exc_info:
            get_resource_from_url(url)

    assert exc_info.value.args[0] == f"Can not convert to json the resource from {url}"


def test_get_resource_from_path(SCHEMA_DIR) -> None:
    path = os.path.join(SCHEMA_DIR, "example.avsc")
    assert get_resource_from_path(path)


def test_get_invalid_resource_from_path(SCHEMA_DIR) -> None:
    path = os.path.join(SCHEMA_DIR, "invalid_resource.txt")
    with pytest.raises(exceptions.JsonRequired) as exc_info:
        get_resource_from_path(path)

    assert exc_info.value.args[0] == f"Can not convert to json the resource from {path}"


def test_get_resource_from_invalid_path() -> None:
    path = os.path.join("example.avsc")
    with pytest.raises(FileNotFoundError):
        get_resource_from_path(path)


def test_validate_resource(example_shema_json) -> None:
    assert validate(schema=example_shema_json)


def test_invalid_schema_format(example_shema_json) -> None:
    # make the json avsc a string so the schema should not be a valid one
    # according to fastavro
    schema = json.dumps(example_shema_json)

    with pytest.raises(exceptions.InvalidSchema) as exc_info:
        validate(schema=schema)

    expected_error = f"Schema {schema} is an unknown type.\n Make sure that its type is a python dictionary"
    assert exc_info.value.args[0] == expected_error


def test_innvalid_schema(invalid_example_shema_json) -> None:
    with pytest.raises(exceptions.InvalidSchema) as exc_info:
        validate(schema=invalid_example_shema_json)

    expected_error = f"Schema {invalid_example_shema_json} is not valid.\n Error: `Default value <1> must match schema type: boolean`"
    assert exc_info.value.args[0] == expected_error
