# Commands

<!-- TOC -->
  * [Validate schema](#validate-schema)
  * [Lint](#lint)
  * [Pre-commit](#pre-commit)
  * [Generate models from schemas](#generate-models-from-schemas)
  * [Serialize data with schema](#serialize-data-with-schema)
  * [Deserialize data with schema](#deserialize-data-with-schema)
  * [View diff between schemas](#view-diff-between-schemas)
  * [Generate fake data from schema](#generate-fake-data-from-schema)
<!-- TOC -->

This section describes all the commands supported by this library together with `dataclasses-avroschema`.
To show the commands we will work with the following schema:

```json
{
  "type": "record",
  "name": "UserAdvance",
  "fields": [
    {
      "name": "name",
      "type": "string"
    },
    {
      "name": "age",
      "type": "long"
    },
    {
      "name": "pets",
      "type": {
        "type": "array",
        "items": "string",
        "name": "pet"
      }
    },
    {
      "name": "accounts",
      "type": {
        "type": "map",
        "values": "long",
        "name": "account"
      }
    },
    {
      "name": "favorite_colors",
      "type": {
        "type": "enum",
        "name": "FavoriteColor",
        "symbols": [
          "BLUE",
          "YELLOW",
          "GREEN"
        ]
      }
    },
    {
      "name": "has_car",
      "type": "boolean",
      "default": false
    },
    {
      "name": "country",
      "type": "string",
      "default": "Argentina"
    },
    {
      "name": "address",
      "type": [
        "null",
        "string"
      ],
      "default": null
    },
    {
      "name": "md5",
      "type": {
        "type": "fixed",
        "name": "md5",
        "size": 16
      }
    }
  ]
}
```

!!! note
All the commands can be executed using a `path` or a `url`

## Validate schema

The previous schema is a valid one.
If we assume that we have a `schema.avsc` in the file system which contains the previous schema we can validate it:

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

If the previous schema is stored in a `schema registry`, for example in `https://schema-registry/schema/1` we can
validate it using the `--url`:

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

If a schema is invalid, for example the following one:

```json
{
  "type": "record",
  "name": "UserAdvance",
  "fields": [
    {
      "name": "name",
      "type": "string"
    },
    {
      "name": "age",
      "type": "long"
    },
    {
      "name": "pets",
      "type": {
        "type": "array",
        "items": "string",
        "name": "pet"
      }
    },
    {
      "name": "accounts",
      "type": {
        "type": "map",
        "values": "long",
        "name": "account"
      }
    },
    {
      "name": "favorite_colors",
      "type": {
        "type": "enum",
        "name": "FavoriteColor",
        "symbols": [
          "BLUE",
          "YELLOW",
          "GREEN"
        ]
      }
    },
    {
      "name": "has_car",
      "type": "boolean",
      "default": 1 #!!!ERROR!!!
    },
    {
      "name": "country",
      "type": "string",
      "default": "Argentina"
    },
    {
      "name": "address",
      "type": [
        "null",
        "string"
      ],
      "default": 10
    },
    {
      "name": "md5",
      "type": {
        "type": "fixed",
        "name": "md5",
        "size": 16
      }
    }
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

## Lint

To check several avro schemas you can use following command

```bash
dc-avro lint tests/schemas/example.avsc tests/schemas/example_v2.avsc
```

and get the following output:

```
👍 Total valid schemas: 2
tests/schemas/example.avsc
tests/schemas/example_v2.avsc
```

For incorrect schema the run is following:

```bash
dc-avro lint tests/schemas/invalid_example.avsc
```

and corresponding output:

```bash
💥 File: tests/schemas/invalid_example.avsc
Schema {'type': 'record', 'name': 'UserAdvance', 'fields': [{'name': 'name', 'type': 'string'}, {'name': 'age', 'type': 'long'}, {'name': 'pets', 'type': {'type': 
'array', 'items': 'string', 'name': 'pet'}}, {'name': 'accounts', 'type': {'type': 'map', 'values': 'long', 'name': 'account'}}, {'name': 'favorite_colors', 'type': 
{'type': 'enum', 'name': 'FavoriteColor', 'symbols': ['BLUE', 'YELLOW', 'GREEN']}}, {'name': 'has_car', 'type': 'boolean', 'default': 1}, {'name': 'country', 'type': 
'string', 'default': 'Argentina'}, {'name': 'address', 'type': ['null', 'string'], 'default': 10}, {'name': 'md5', 'type': {'type': 'fixed', 'name': 'md5', 'size': 
16}}]} is not valid.
 Error: `Default value <1> must match schema type: boolean`
╭─────────────────────────────── Traceback (most recent call last) ────────────────────────────────╮
│ ~/dc-avro/dc_avro/main.py:176 in lint                                 │
│                                                                                                  │
│   173 │   │   │   console.print(":boom: File: " + error_path)                                    │
│   174 │   │   │   console.print(f"[red]{error}[/red]")                                           │
│   175 │   │   app.pretty_exceptions_show_locals = False                                          │
│ ❱ 176 │   │   raise InvalidSchema(error_msg)                                                     │
│   177                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
InvalidSchema: Total errors detected: 1
```

## Pre-commit

Add the following lines to your `.pre-commit-config.yaml` file to enable avro schemas linting

```yaml
  - repo: https://github.com/marcosschroh/dc-avro.git
    rev: 0.7.0
    hooks:
      - id: lint-avsc
        additional_dependencies: [typing_extensions]
```

## Generate models from schemas

Python models can be generated using the command `generate-model`. This command also works with `path` and `url`.
It is also possible to provide the `--model-type` that will be used in the `models`. This models can be `[dataclass|pydantic|avrodantic]`

=== "Dataclass models"

    ```python
    dc-avro generate-model --path tests/schemas/example.avsc

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

        class Meta:
            field_order = ['name', 'age', 'pets', 'accounts', 'favorite_colors', 'has_car', 'country', 'address', 'md5']
    ```

=== "Pydantic models"

    ```python
    dc-avro generate-model --path tests/schemas/example.avsc --model-type pydantic

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

        class Meta:
            field_order = ['name', 'age', 'pets', 'accounts', 'favorite_colors', 'has_car', 'country', 'address', 'md5']
    ```

=== "Avrodantic (avro + pydantic)"

    ```python
    dc-avro generate-model --path tests/schemas/example.avsc --model-type avrodantic

    from dataclasses_avroschema import types
    from pydantic import BaseModel
    import enum
    import typing


    class FavoriteColor(enum.Enum):
        BLUE = "BLUE"
        YELLOW = "YELLOW"
        GREEN = "GREEN"


    class UserAdvance(AvroBaseModel):
        name: str
        age: int
        pets: typing.List
        accounts: typing.Dict
        favorite_colors: FavoriteColor
        md5: types.Fixed = types.Fixed(16)
        has_car: bool = False
        country: str = "Argentina"
        address: typing.Optional = None

        class Meta:
            field_order = ['name', 'age', 'pets', 'accounts', 'favorite_colors', 'has_car', 'country', 'address', 'md5']
    ```

!!! note
    If you want to save the result to a local file you can execute `dc-avro generate-model --path schema.avsc > my-models.py`

## Serialize data with schema

We can `serialize` the data with schemas either in `avro` or `avro-json`, for example:

```bash title="Event"
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
The data provided to the command must be wrapped in quotes as it is interpreted as a string and then converted to a
python `dict`

## Deserialize data with schema

We can `deserialize` the data with schemas either in `avro` or `avro-json`, for example:

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
For  `avro deserialization` you have to include the character `b` in the string to indicate that the actual value
is `bytes`

## View diff between schemas

Sometimes it is useful to see the difference between `avsc` files, specially for the `avro schema evolution`. You need to specify the `source` and `target` schema.
Both of them can be using the `path` or `url`

Example:

The v1 schema version is in the `schema registry`:

```json
{
  "type": "record",
  "name": "UserAdvance",
  "fields": [
    {
      "name": "name",
      "type": "string"
    },
    {
      "name": "age",
      "type": "long"
    },
    {
      "name": "pets",
      "type": {
        "type": "array",
        "items": "string",
        "name": "pet"
      }
    },
    {
      "name": "accounts",
      "type": {
        "type": "map",
        "values": "long",
        "name": "account"
      }
    },
    {
      "name": "favorite_colors",
      "type": {
        "type": "enum",
        "name": "FavoriteColor",
        "symbols": [
          "BLUE",
          "YELLOW",
          "GREEN"
        ]
      }
    },
    {
      "name": "has_car",
      "type": "boolean",
      "default": false
    },
    {
      "name": "country",
      "type": "string",
      "default": "Argentina"
    },
    {
      "name": "address",
      "type": [
        "null",
        "string"
      ],
      "default": null
    },
    {
      "name": "md5",
      "type": {
        "type": "fixed",
        "name": "md5",
        "size": 16
      }
    }
  ]
}
```

Then a PR has been opened with the `UserAdvance v2`:

```json
{
  "type": "record",
  "name": "UserAdvance",
  "fields": [
    {
      "name": "name",
      "type": "string"
    },
    {
      "name": "age",
      "type": "long"
    },
    {
      "name": "pets",
      "type": {
        "type": "array",
        "items": "string",
        "name": "pet"
      }
    },
    {
      "name": "accounts",
      "type": {
        "type": "map",
        "values": "long",
        "name": "account"
      }
    },
    {
      "name": "favorite_colors",
      "type": {
        "type": "enum",
        "name": "FavoriteColor",
        "symbols": [
          "BLUE",
          "YELLOW",
          "GREEN"
        ]
      }
    },
    {
      "name": "has_car",
      "type": "boolean",
      "default": false
    },
    {
      "name": "country",
      "type": "string",
      "default": "Netherlands"
    },
    {
      "name": "address",
      "type": [
        "null",
        "string"
      ],
      "default": null
    }
  ]
}
```

- We can see that the `default` value for `country` has been updated from `Argentina` to `Netherlads`
- The field `md5` has been removed

If we run the `schema-diff` command we have the following result:

```bash
dc-avro schema-diff --source-path ./tests/schemas/example.avsc --target-path  ./tests/schemas/example_v2.avsc
```

![type:video](statics/schema_diff.mov)

By default the whole files are shown. You can provide the option `--only-deltas` to see only the lines that has changed. The command gives a `default` context of `5` lines. To provide more or less context you can use the parameter `--num-lines`

```bash
dc-avro schema-diff --source-path ./tests/schemas/example.avsc --target-path  ./tests/schemas/example_v2.avsc --only-deltas --num-lines 3
```

![type:video](statics/schema_diff_deltas.mov)

## Generate fake data from schema

Generate one sample from a given schema:

```bash
dc-avro generate-data ./tests/schemas/example.avsc
```

To generate many fake data, add the `count` parameter:

```bash
dc-avro generate-data ./tests/schemas/example.avsc --count 3
```

Keep in mind that you can provide a filepath or a url

Help:

```bash
$ dc-avro generate-data --help

Usage: dc-avro generate-data [OPTIONS] [RESOURCE]

 Generate fake data for a given avsc schema

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│   resource      [RESOURCE]  Path or URL to the avro schema [default: None]                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --count        INTEGER  Number of data to generate, more than one prints a list [default: 1]                                            │
│ --help                  Show this message and exit.                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
