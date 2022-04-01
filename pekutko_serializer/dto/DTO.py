from dataclasses import dataclass


@dataclass
class DTO_TYPES():
    FUNC = "func"
    CLASS = "class"
    OBJ = "obj"
    VAR = "var"
    LIST = "list"
    DICT = "dict"
    TUPLE = "tuple"
    LITERAL = "literal"


@dataclass
class DTO():
    dto_type = "DTO_TYPE"
    name = "name"
    value = "value"
    code = "code"
    global_names = "globals"
    based_class = "based_class"
