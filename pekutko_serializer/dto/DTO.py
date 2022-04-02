from dataclasses import dataclass


@dataclass
class DTO_TYPES():
    FUNC = "func"
    CLASS = "class"
    OBJ = "obj"
    DICT = "dict"

@dataclass
class DTO():
    dto_type = "DTO_TYPE"
    name = "name"
    fields = "fields"
    code = "code"
    global_names = "globals"
    base_class = "class"
