from .serialize import JSON_SER_TYPES
import json
import types

def _parse_class(class_dict):
    class_name = class_dict["@name"]
    class_members_dict = class_dict["@dict"]
    for member in class_members_dict.items():
        if JSON_SER_TYPES["function"] in member[1]:
            func_dict = member[1][JSON_SER_TYPES["function"]]
            class_members_dict[func_dict["@name"]] = _parse_func(func_dict)
    return type(class_name, (object, ), class_members_dict)

def _parse_obj(obj_dict: dict):
    obj_class = _parse_class(obj_dict[JSON_SER_TYPES["class"]])
    obj = obj_class()
    obj.__dict__ = obj_dict["@dict"]
    return obj 

def _parse_func(func_dict):
    func_name = func_dict["@name"]
    func_globals = func_dict["@globals"]
    for glob in func_globals.items():
        if type(glob[1]) is dict:
            if JSON_SER_TYPES["function"] in glob[1]:
                func_globals[glob[0]] = _parse_func(glob[1][JSON_SER_TYPES["function"]])
    code_type =  types.CodeType(
        func_dict["co_argcount"],
        func_dict["co_posonlyargcount"],
        func_dict["co_kwonlyargcount"],
        func_dict["co_nlocals"],
        func_dict["co_stacksize"],
        func_dict["co_flags"],
        bytes(func_dict["co_code"]),
        tuple(func_dict["co_consts"]),
        tuple(func_dict["co_names"]),
        tuple(func_dict["co_varnames"]),
        func_dict["co_filename"],
        func_name,
        func_dict["co_firstlineno"],
        bytes(func_dict["co_lnotab"]),
        tuple(func_dict["co_freevars"]),
        tuple(func_dict["co_cellvars"])
    )
    return types.FunctionType(code_type, func_globals, func_name)

def _parse(_str):
    _dict = json.loads(_str)
    if JSON_SER_TYPES["class"] in _dict:
        return _parse_class(_dict[JSON_SER_TYPES["class"]])
    elif JSON_SER_TYPES["object"] in _dict:
        return _parse_obj(_dict[JSON_SER_TYPES["object"]])
    elif JSON_SER_TYPES["function"] in _dict:
        return _parse_func(_dict[JSON_SER_TYPES["function"]])

def deserialize(_str):
    return _parse(_str)