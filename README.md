# Dataclasses Avro Schema CLI

Command line interface from [dataclasses-avroschema](https://github.com/marcosschroh/dataclasses-avroschema) to work with `avsc` resources

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fmarcosschroh%2Fdc-avro%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/marcosschroh/dc-avro/goto?ref=master)
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
* [] Generate `models` from `schemas`
* [] View diff between `schemas`
* [] Generate fake data from `schema`
* [] Encode data with `schema`

## Development

1. Create a `virtualenv`: `python3.7 -m venv venv && source venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Code linting: `./scripts/format`
4. Run tests: `./scripts/test`
