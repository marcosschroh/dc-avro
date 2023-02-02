import enum
import typing

JsonDict = typing.Dict[str, typing.Any]

# Move this to dataclasses-avroschema
class SerializationType(str, enum.Enum):
    AVRO = "avro"
    AVRO_JSON = "avro-json"
