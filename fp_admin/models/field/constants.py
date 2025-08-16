from typing import Literal

FieldType = Literal[
    "string",
    "number",
    "float",
    "time",
    "datetime",
    "boolean",
    "file",
    "date",
    "json",
    "password",
    "choice",
    "multichoice",
    "foreign_key",
    "many_to_many",
    "one_to_one",
    "primary_key",
]

RELATIONSHIP_FIELD_TYPES = [
    "foreign_key",
    "many_to_many",
    "one_to_one",
]
