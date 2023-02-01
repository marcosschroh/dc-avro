import os
from unittest import mock

from httpx import Response, codes
from typer.testing import CliRunner

from dc_avro._types import JsonDict
from dc_avro.main import app

runner = CliRunner()

url = "https://schema-registry/example.avsc"


def test_validate_schema_from_path(SCHEMA_DIR: str):
    result = runner.invoke(
        app, ["validate-schema", "--path", os.path.join(SCHEMA_DIR, "example.avsc")]
    )
    assert result.exit_code == 0
    assert "Valid schema!!" in result.stdout


def test_validate_schema_from_url(example_shema_json: JsonDict):
    responnse = Response(status_code=codes.OK, json=example_shema_json)
    with mock.patch("dc_avro.main._schema_utils.httpx.get", return_value=responnse):
        result = runner.invoke(app, ["validate-schema", "--url", url])
        assert result.exit_code == 0
        assert "Valid schema!!" in result.stdout


def test_validate_schema_invalid_path(SCHEMA_DIR):
    result = runner.invoke(
        app,
        ["validate-schema", "--path", os.path.join(SCHEMA_DIR, "invalid_example.avsc")],
    )
    assert result.exit_code == 1

    result = runner.invoke(
        app,
        ["validate-schema", "--url", "https://google.com"],
    )
    assert result.exit_code == 1


def test_invalid_schema_two_options(SCHEMA_DIR: str):
    result = runner.invoke(
        app,
        [
            "validate-schema",
            "--path",
            os.path.join(SCHEMA_DIR, "invalid_example.avsc"),
            "--url",
            "https://some.url",
        ],
    )
    assert result.exit_code == 2


def test_generate_model_from_path(SCHEMA_DIR: str, model_generator_output_command: str):
    result = runner.invoke(
        app, ["generate-model", "--path", os.path.join(SCHEMA_DIR, "example.avsc")]
    )
    assert result.exit_code == 0
    assert model_generator_output_command == result.stdout


def test_generate_model_from_url(
    example_shema_json: JsonDict, model_generator_output_command: str
):
    responnse = Response(status_code=codes.OK, json=example_shema_json)
    with mock.patch("dc_avro.main._schema_utils.httpx.get", return_value=responnse):
        result = runner.invoke(app, ["generate-model", "--url", url])
        assert result.exit_code == 0
        assert model_generator_output_command == result.stdout


def test_generate_model_two_options(SCHEMA_DIR: str):
    result = runner.invoke(
        app,
        [
            "generate-model",
            "--path",
            os.path.join(SCHEMA_DIR, "invalid_example.avsc"),
            "--url",
            "https://some.url",
        ],
    )
    assert result.exit_code == 2
