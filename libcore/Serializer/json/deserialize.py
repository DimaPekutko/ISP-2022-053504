from .serialize import JSON_SER_TYPES
import json
import inspect

def _parse_class(class_dict):
    class_name = class_dict["name"]
    class_members_dict = class_dict["dict"]
    for member in class_members_dict.items():
        if JSON_SER_TYPES["function"] in member[1]:
            func_dict = member[1][JSON_SER_TYPES["function"]]
            # print(member)
    return type(class_name, (object, ), class_members_dict)

def _parse_obj(obj_dict: dict):
    _class = _parse_class(obj_dict[JSON_SER_TYPES["class"]])

def _parse_func(func_dict):
    pass

def _parse(_str):
    _dict = json.loads(_str)
    if JSON_SER_TYPES["class"] in _dict:
        _parse_class(_dict[JSON_SER_TYPES["class"]])
    elif JSON_SER_TYPES["object"] in _dict:
        _parse_obj(_dict[JSON_SER_TYPES["object"]])
    elif JSON_SER_TYPES["function"] in _dict:
        _parse_func(_dict[JSON_SER_TYPES["function"]])

def deserialize(_str):
    return _parse(_str)