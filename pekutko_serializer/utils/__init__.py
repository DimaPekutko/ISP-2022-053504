import inspect
import re
from types import BuiltinFunctionType, CodeType, GetSetDescriptorType, MappingProxyType, MethodDescriptorType, ModuleType, WrapperDescriptorType


def get_actual_func_globals(func) -> dict:
    code = func.__code__
    func_globals = func.__globals__.items()
    actual_globals = {}
    for glob in func_globals:
        if glob[0] in code.co_names:
            actual_globals.update({glob[0]: glob[1]})
    return actual_globals


def get_actual_code_fields(_code: CodeType) -> dict:
    code_dict = {}
    for member in inspect.getmembers(_code):
        if str(member[0]).startswith("co_"):
            code_dict.update({member[0]: member[1]})
    return code_dict


def get_actual_module_fields(module: ModuleType) -> dict:
    module_fields = {}
    module_members = inspect.getmembers(module)
    for mem in module_members:
        if not mem[0].startswith("__"):
            module_fields.update({mem[0]: mem[1]})
    return module_fields


def get_actual_class_fields(_class: type) -> dict:
    fields_dict = {}
    if _class == type:
        fields_dict.update({
            "__bases__": [],
        })
    else:
        mems = inspect.getmembers(_class)
        for mem in mems:
            if type(mem[1]) not in (
                WrapperDescriptorType,
                MethodDescriptorType,
                BuiltinFunctionType,
                MappingProxyType,
                GetSetDescriptorType
            ):
                if mem[0] not in (
                    "__mro__", "__base__", "__basicsize__",
                    "__class__", "__dictoffset__", "__name__",
                    "__qualname__", "__text_signature__", "__itemsize__",
                    "__flags__", "__weakrefoffset__"
                ):
                    fields_dict.update({mem[0]: mem[1]})
    return fields_dict