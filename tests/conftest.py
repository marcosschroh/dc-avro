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
def schema_dir():
    return AVRO_SCHEMAS_DIR


@pytest.fixture
def example_schema_json():
    return load_json("example.avsc")


@pytest.fixture
def invalid_example_schema_json():
    return load_json("invalid_example.avsc")


@pytest.fixture
def invalid_resource():
    return load("invalid_resource.txt")


@pytest.fixture
def model_generator_output_dataclass():
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
    pets: typing.List[str]
    accounts: typing.Dict[str, int]
    favorite_colors: FavoriteColor
    md5: types.confixed(size=16)
    has_car: bool = False
    country: str = "Argentina"
    address: typing.Optional[str] = None

    class Meta:
        field_order = ['name', 'age', 'pets', 'accounts', 'favorite_colors', 'has_car', 'country', 'address', 'md5']

"""
    return result


@pytest.fixture
def model_generator_output_pydantic():
    result = """from dataclasses_avroschema import types
from pydantic import BaseModel
import enum
import typing


class FavoriteColor(enum.Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"



class UserAdvance(BaseModel):
    name: str
    age: int
    pets: typing.List[str]
    accounts: typing.Dict[str, int]
    favorite_colors: FavoriteColor
    md5: types.confixed(size=16)
    has_car: bool = False
    country: str = "Argentina"
    address: typing.Optional[str] = None

    class Meta:
        field_order = ['name', 'age', 'pets', 'accounts', 'favorite_colors', 'has_car', 'country', 'address', 'md5']

"""
    return result


@pytest.fixture
def model_generator_output_avrodantic():
    result = """from dataclasses_avroschema import types
from dataclasses_avroschema.pydantic import AvroBaseModel
import enum
import typing


class FavoriteColor(enum.Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"



class UserAdvance(AvroBaseModel):
    name: str
    age: int
    pets: typing.List[str]
    accounts: typing.Dict[str, int]
    favorite_colors: FavoriteColor
    md5: types.confixed(size=16)
    has_car: bool = False
    country: str = "Argentina"
    address: typing.Optional[str] = None

    class Meta:
        field_order = ['name', 'age', 'pets', 'accounts', 'favorite_colors', 'has_car', 'country', 'address', 'md5']

"""
    return result
