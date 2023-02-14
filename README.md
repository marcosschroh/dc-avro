# Dataclasses Avro Schema CLI

Command line interface from [dataclasses-avroschema](https://github.com/marcosschroh/dataclasses-avroschema) to work with `avsc` resources

[![Tests](https://github.com/marcosschroh/dc-avro/actions/workflows/tests.yaml/badge.svg)](https://github.com/marcosschroh/dc-avro/actions/workflows/tests.yaml)
[![GitHub license](https://img.shields.io/github/license/marcosschroh/dc-avro.svg)](https://github.com/marcosschroh/dc-avro/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/marcosschroh/dc-avro/branch/master/graph/badge.svg)](https://codecov.io/gh/marcosschroh/dc-avro)
![python version](https://img.shields.io/badge/python-3.7%2B-yellowgreen)

## Requirements

`python 3.7+`

## Documentation

https://marcosschroh.github.io/dc-avro/

## Usage

You can validate `avro schemas` either from a `local file` or `url`:

Assuming that we have a local file `schema.avsc` that contains an `avro schema`, we can check whether it is valid

```bash
dc-avro validate-schema --path schema.avsc

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

To see all the commands execute `dc-avro --help`

## Features

* [x] Validate `schemas`
* [x] Generate `models` from `schemas`
* [x] Data deserialization with `schema`
* [x] Data serialization with `schema`
* [x] View diff between `schemas`
* [] Generate fake data from `schema`

## Development

1. Install requirements: `poetry install`
2. Code linting: `./scripts/format`
3. Run tests: `./scripts/test`
