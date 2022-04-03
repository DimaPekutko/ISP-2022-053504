from dataclasses import dataclass


@dataclass
class DTO_TYPES():
    FUNC = "func"
    MODULE = "module"
    CLASS = "class"
    OBJ = "obj"
    DICT = "dict"
    MIRROR_DICT = "mirror_dict"

@dataclass
class DTO():
    dto_type = "DTO_TYPE"
    name = "name"
    fields = "fields"
    path = "path"
    code = "code"
    global_names = "globals"
    base_class = "class"
