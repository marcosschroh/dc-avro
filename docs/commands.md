# Commands

This section describes all the commands supported by this library together with `dataclasses-avroschema`. To show the commands we will work with the following schema:

```python
{
    'type': 'record',
    'name': 'UserAdvance',
    'fields': [
        {'name': 'name', 'type': 'string'},
        {'name': 'age', 'type': 'long'},
        {'name': 'pets', 'type': {'type': 'array', 'items': 'string', 'name': 'pet'}},
        {'name': 'accounts', 'type': {'type': 'map', 'values': 'long', 'name': 'account'}},
        {'name': 'favorite_colors', 'type': {'type': 'enum', 'name': 'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}},
        {'name': 'has_car', 'type': 'boolean', 'default': False},
        {'name': 'country', 'type': 'string', 'default': 'Argentina'},
        {'name': 'address', 'type': ['null', 'string'], 'default': None},
        {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}
    ]
}
```

!!! note
    All the commands can be executed using a `path` or a `url`

## Validate schemas

The previous schema is a valid one. If we assume that we have a `schema.avsc` in the file system which contains the previous schema we can validate it:

```bash
dc-avro validate-schema --path schema.avsc
```

resulting in

```bash
Valid schema!! 👍 

{
    'type': 'record',
    'name': 'UserAdvance',
    'fields': [
        {'name': 'name', 'type': 'string'},
        {'name': 'age', 'type': 'long'},
        {'name': 'pets', 'type': {'type': 'array', 'items': 'string', 'name': 'pet'}},
        {'name': 'accounts', 'type': {'type': 'map', 'values': 'long', 'name': 'account'}},
        {'name': 'favorite_colors', 'type': {'type': 'enum', 'name': 'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}},
        {'name': 'has_car', 'type': 'boolean', 'default': False},
        {'name': 'country', 'type': 'string', 'default': 'Argentina'},
        {'name': 'address', 'type': ['null', 'string'], 'default': None},
        {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}
    ]
}
```

If the previous schema is stored in a `schema registry`, for example in `https://schema-registry/schema/1` we can validate it using the `--url`:

```bash
dc-avro validate-schema --url https://schema-registry/schema/1
```

resulting in

```bash
Valid schema!! 👍 

{
    'type': 'record',
    'name': 'UserAdvance',
    'fields': [
        {'name': 'name', 'type': 'string'},
        {'name': 'age', 'type': 'long'},
        {'name': 'pets', 'type': {'type': 'array', 'items': 'string', 'name': 'pet'}},
        {'name': 'accounts', 'type': {'type': 'map', 'values': 'long', 'name': 'account'}},
        {'name': 'favorite_colors', 'type': {'type': 'enum', 'name': 'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}},
        {'name': 'has_car', 'type': 'boolean', 'default': False},
        {'name': 'country', 'type': 'string', 'default': 'Argentina'},
        {'name': 'address', 'type': ['null', 'string'], 'default': None},
        {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}
    ]
}
```

If an schema is invalid, for example the folling one:

```bash
{
    "type": "record",
    "name": "UserAdvance",
    "fields": [
      {"name": "name", "type": "string"},
      {"name": "age", "type": "long"},
      {"name": "pets", "type": {"type": "array", "items": "string", "name": "pet"}},
      { "name": "accounts", "type": { "type": "map", "values": "long", "name": "account"}},
      {"name": "favorite_colors", "type": {"type": "enum", "name": "FavoriteColor", "symbols": ["BLUE", "YELLOW", "GREEN"]}},
      {"name": "has_car", "type": "boolean", "default": 1}, # ERROR!!!!
      { "name": "country", "type": "string", "default": "Argentina"},
      {"name": "address", "type": ["null", "string"], "default": 10},
      {"name": "md5", "type": {"type": "fixed", "name": "md5", "size": 16}}
    ]
  }
```

The result will be:

```bash
InvalidSchema: Schema {'type': 'record', 'name': 'UserAdvance', 'fields': [{'name': 'name', 'type': 'string'}, {'name': 'age', 
'type': 'long'}, {'name': 'pets', 'type': {'type': 'array', 'items': 'string', 'name': 'pet'}}, {'name': 'accounts', 'type': 
{'type': 'map', 'values': 'long', 'name': 'account'}}, {'name': 'favorite_colors', 'type': {'type': 'enum', 'name': 
'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}}, {'name': 'has_car', 'type': 'boolean', 'default': 1}, {'name': 
'country', 'type': 'string', 'default': 'Argentina'}, {'name': 'address', 'type': ['null', 'string'], 'default': 10}, {'name': 
'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}]} is not valid.
 Error: `Default value <1> must match schema type: boolean`
```

## Generate models from schemas

Python models can be generated using the command `generate-model`. This command also works with `path` and `url`. It is also possible to provide the `base-class` that will be use in the `models`. This base class can be `[AvroModel|BaseModel|AvroBaseModel]`

[![asciicast](https://asciinema.org/a/557200.svg)](https://asciinema.org/a/557200)

=== "Dataclass models"

    ```python
    dc-avro generate-model --path schema.avsc

    from dataclasses_avroschema import AvroModel
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
    ```

=== "Pydantic models"

    ```python
    dc-avro generate-model --path schema.avsc --base-class BaseModel

    from dataclasses_avroschema import types
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
        pets: typing.List
        accounts: typing.Dict
        favorite_colors: FavoriteColor
        md5: types.Fixed = types.Fixed(16)
        has_car: bool = False
        country: str = "Argentina"
        address: typing.Optional = None
    ```

!!! note
    If you want to save the result to a local file you can execute `dc-avro generate-model --path schema.avsc > my-models.py`

## Serialize data with schema

We can `serialize` data with schemas either in `avro` or `avro-json`, for example:

```python title="Event"
{'name': 'bond', 'age': 50, 'pets': ['dog', 'cat'], 'accounts': {'key': 1}, 'has_car': False, 'favorite_colors': 'BLUE', 'country': 'Argentina', 'address': None, 'md5': b'u00ffffffffffffx'}
```

=== "avro serialization"

    ```python
    dc-avro serialize "{'name': 'bond', 'age': 50, 'pets': ['dog', 'cat'], 'accounts': {'key': 1}, 'has_car': False, 'favorite_colors': 'BLUE', 'country': 'Argentina', 'address': None, 'md5': b'u00ffffffffffffx'}" --path ./tests/schemas/example.avsc

    b'\x08bondd\x04\x06dog\x06cat\x00\x02\x06key\x02\x00\x00\x00\x12Argentina\x00u00ffffffffffffx'
    ``` 

=== "avro-json serialization"

    ```python
    dc-avro serialize "{'name': 'bond', 'age': 50, 'pets': ['dog', 'cat'], 'accounts': {'key': 1}, 'has_car': False, 'favorite_colors': 'BLUE', 'country': 'Argentina', 'address': None, 'md5': b'u00ffffffffffffx'}" --path ./tests/schemas/example.avsc --serialization-type avro-json

    b'{"name": "bond", "age": 50, "pets": ["dog", "cat"], "accounts": {"key": 1}, "favorite_colors": "BLUE", "has_car": false, "country": 
    "Argentina", "address": null, "md5": "u00ffffffffffffx"}'
    ```

!!! note
    The data provided to the command must be wrapped in quotes as it is interpreted as a string and then converted to a python `dict`

## Deserialize data with schema

We can `deserialize` data with schemas either in `avro` or `avro-json`, for example:

=== "avro deserialization"

    ```python
    dc-avro deserialize 'b"\x08bondd\x04\x06dog\x06cat\x00\x02\x06key\x02\x00\x00\x00\x12Argentina\x00u00ffffffffffffx"' --path ./tests/schemas/example.avsc

    {
        'name': 'bond',
        'age': 50,
        'pets': ['dog', 'cat'],
        'accounts': {'key': 1},
        'favorite_colors': 'BLUE',
        'has_car': False,
        'country': 'Argentina',
        'address': None,
        'md5': b'u00ffffffffffffx'
    }
    ``` 

=== "avro-json deserialization"

    ```python
    dc-avro deserialize '{"name": "bond", "age": 50, "pets": ["dog", "cat"], "accounts": {"key": 1}, "favorite_colors": "BLUE", "has_car": false, "country":  "Argentina", "address": null, "md5": "u00ffffffffffffx"}' --path ./tests/schemas/example.avsc --serialization-type avro-json

    {
        'name': 'bond',
        'age': 50,
        'pets': ['dog', 'cat'],
        'accounts': {'key': 1},
        'favorite_colors': 'BLUE',
        'has_car': False,
        'country': 'Argentina',
        'address': None,
        'md5': b'u00ffffffffffffx'
    }
    ```

!!! note
    For  `avro deserialization` you have to include the character `b` in the string to indicate that the actual value is `bytes`

## View diff between schemas

Sometimes it is useful to see the difference between `avsc` files, specially for the `avro schema evolution`. You need to specify the `source` and `target` schema.
Both of them can be using the `path` or `url`

Example:

The v1 schema version is in the `schema registry`:

```python
{
    'type': 'record',
    'name': 'UserAdvance',
    'fields': [
        {'name': 'name', 'type': 'string'},
        {'name': 'age', 'type': 'long'},
        {'name': 'pets', 'type': {'type': 'array', 'items': 'string', 'name': 'pet'}},
        {'name': 'accounts', 'type': {'type': 'map', 'values': 'long', 'name': 'account'}},
        {'name': 'favorite_colors', 'type': {'type': 'enum', 'name': 'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}},
        {'name': 'has_car', 'type': 'boolean', 'default': False},
        {'name': 'country', 'type': 'string', 'default': 'Argentina'},
        {'name': 'address', 'type': ['null', 'string'], 'default': None},
        {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}
    ]
}
```

Then a PR has been opened with the `UserAdvance v2`:

```python
{
    "type": "record",
    "name": "UserAdvance",
    "fields": [
      {"name": "name", "type": "string"},
      {"name": "age", "type": "long"},
      {"name": "pets", "type": { "type": "array", "items": "string", "name": "pet"}},
      {"name": "accounts", "type": { "type": "map", "values": "long", "name": "account"}},
      {"name": "favorite_colors", "type": {"type": "enum", "name": "FavoriteColor", "symbols": ["BLUE", "YELLOW", "GREEN"]}},
      {"name": "has_car", "type": "boolean", "default": False},
      {"name": "country", "type": "string", "default": "Netherlands"},
      {"name": "address", "type": ["null", "string"], "default": None}
    ]
  }
```

- We can see that the `default` value for `country` has been updated from `Argentina` to `Netherlads`
- The field `md5` has been removed

If we run the `schema-diff` command we have the following result:

```bash
dc-avro schema-diff --source-path ./tests/schemas/example.avsc --target-path  ./tests/schemas/example_v2.avsc

{
    'values_changed': {"root['fields'][6]['default']": {'new_value': 'Netherlands', 'old_value': 'Argentina'}},
    'iterable_item_removed': {"root['fields'][8]": {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 16}}}
}
```

## Generate fake data from schema

🚧🚧🚧🚧🚧
