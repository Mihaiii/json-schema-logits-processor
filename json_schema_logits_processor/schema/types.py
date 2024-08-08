from enum import Enum


class SchemaType(Enum):
    STRING = 0
    NUMBER = 1
    OBJECT = 2
    ENUM = 3
    ARRAY = 4

    # BOOLEAN = "boolean"
    # ARRAY = "array"
    # NULL = "null"
