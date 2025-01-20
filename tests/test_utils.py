import os
from unittest import mock

from httpx import Response, codes

from dc_avro._schema_utils import get_raw_resource_from_path, get_raw_resource_from_url


def test_get_raw_resource_from_path(schema_dir: str) -> None:
    with open(os.path.join(schema_dir, "example.avsc"), "r") as file:
        schema = file.readlines()

    resource_path = os.path.join(schema_dir, "example.avsc")
    result = get_raw_resource_from_path(resource_path)

    assert result == schema


def test_get_raw_resource_from_url(schema_dir: str) -> None:
    with open(os.path.join(schema_dir, "example.avsc"), "r") as file:
        schema = file.read()

    response = Response(status_code=codes.OK, text=schema)
    with mock.patch("dc_avro.main._schema_utils.httpx.get", return_value=response):
        result = get_raw_resource_from_url("http://example.com")

    assert result == schema.splitlines()
