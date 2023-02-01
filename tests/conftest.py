import json
import os

import pytest

AVRO_SCHEMAS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schemas")


def load(file_name):
    path = os.path.join(AVRO_SCHEMAS_DIR, file_name)
    with open(path, mode="r") as f:
        return f.read()


def load_json(file_name):
    schema_string = load(file_name)
    return json.loads(schema_string)


@pytest.fixture
def SCHEMA_DIR():
    return AVRO_SCHEMAS_DIR


@pytest.fixture
def example_shema_json():
    return load_json("example.avsc")


@pytest.fixture
def invalid_example_shema_json():
    return load_json("invalid_example.avsc")


@pytest.fixture
def invalid_resource():
    return load("invalid_resource.txt")


@pytest.fixture
def model_generator_output_command():
    result = """from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import enum
import typing


class FavoriteColor(enum.Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


@dataclasses.dataclass
class UserAdvance(AvroModel):
    name: str
    age: int
    pets: typing.List
    accounts: typing.Dict
    favorite_colors: FavoriteColor
    md5: types.Fixed = types.Fixed(16)
    has_car: bool = False
    country: str = "Argentina"
    address: typing.Optional = None

"""
    return result
