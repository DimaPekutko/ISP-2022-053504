
import inspect
from types import BuiltinFunctionType, GetSetDescriptorType, MappingProxyType, MethodDescriptorType, ModuleType, WrapperDescriptorType

from pekutko_serializer.dto import DTO, DTO_TYPES
from ..BaseSerializer import BaseSerializer


class TomlSerializer(BaseSerializer):
    __res_str = ""
    __container_names = []
    __parser = None

    def __init__(self):
        super().__init__()
        # self.__parser = JsonParser()

    def dumps(self, obj: any) -> str:
        # self.__res_str = ""
        self._visit(obj)
        return self.__res_str

    def dump(self, obj: any, file_path: str):
        pass

    def loads(self, source: str) -> any:
        return self.__parser.parse(source)

    def load(self, file_path: str) -> any:
        pass

    def _put(self, s: str):
        self.__res_str += s

    def _push_name(self, s: str):
        self.__container_names.append(s)

    def _pop_name(self) -> str:
        return self.__container_names.pop()

    def _get_concat_name(self) -> str:
        return ".".join(self.__container_names)

    def _is_primitive_type(self, obj: any) -> bool:
        _type = type(obj)
        if _type in (int, float, str, bool, bytes) or obj == None:
            return True
        elif _type in (tuple, list):
            if len(obj) >= 1:
                return self._is_primitive_type(obj[0])
            else:
                return True
        return False

    def _divide_dict_by_primitive(self, _dict: dict) -> tuple:
        prim_dict = {}
        complex_dict = {}
        for item in _dict.items():
            if self._is_primitive_type(item[1]):
                prim_dict.update({item[0]: item[1]})
            else:
                complex_dict.update({item[0]: item[1]})
        return prim_dict, complex_dict

    def _visit_func_globals(self, func):
        code = func.__code__
        func_globals = func.__globals__.items()
        actual_globals = {}
        for glob in func_globals:
            if glob[0] in code.co_names:
                actual_globals.update({glob[0]: glob[1]})
        self._visit(actual_globals, DTO.global_names)

    def _visit_func_code(self, func):
        code = func.__code__
        code_dict = {}
        for member in inspect.getmembers(code):
            if str(member[0]).startswith("co_"):
                code_dict.update({member[0]: member[1]})
        self._visit(code_dict, DTO.code)

    def _visit_func(self, func):
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.FUNC}"\n')
        self._put(f'{DTO.name} = "{func.__name__}"\n\n')
        self._visit_func_globals(func)
        self._visit_func_code(func)
        pass

    def _visit_module(self, module):
        module_fields = {}
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.MODULE}"\n')
        self._put(f'{DTO.name} = "{module.__name__}"\n\n')
        module_members = inspect.getmembers(module)
        for mem in module_members:
            if not mem[0].startswith("__"):
                module_fields.update({mem[0]: mem[1]})
        self._visit(module_fields, DTO.fields)

    def _visit_class(self, _class):
        self._put(f'{DTO.dto_type} = "{DTO_TYPES.CLASS}"\n')
        self._put(f'{DTO.name} = "{_class.__name__}"\n\n')
        # self._put(f'"{DTO.fields}": ')
        mems = inspect.getmembers(_class)
        fields_dict = {}
        for mem in mems:
            if type(mem[1]) not in (
                WrapperDescriptorType,
                MethodDescriptorType,
                BuiltinFunctionType,
                MappingProxyType,
                GetSetDescriptorType
            ):
                if mem[1] != None and mem[1] != type:
                    fields_dict.update({mem[0]: mem[1]})
        self._visit(fields_dict, DTO.fields)
        pass

    def _visit_obj(self, obj):
        # print(obj)
        self._put(f'{DTO.dto_type} =  "{DTO_TYPES.OBJ}"\n\n')
        self._visit(obj.__class__, DTO.base_class)
        self._visit(obj.__dict__, DTO.fields)
        pass

    def _visit_dict(self, _dict: dict):
        # sorting dict to set primitive fields at the begining
        prim_dict, complex_dict = self._divide_dict_by_primitive(_dict)

        self._put(f'{DTO.dto_type} = "{DTO_TYPES.DICT}"\n')

        for prim in prim_dict.items():
            self._put(f'{prim[0]} = ')
            self._visit(prim[1])
            self._put("\n")

        self._put("\n")

        for comp in complex_dict.items():
            self._visit(comp[1], comp[0])
            self._put("\n")

    def _visit_primitive(self, prim_obj):
        _type = type(prim_obj)
        if _type in (int, float):
            self._put(f'{prim_obj}')
        elif _type == str:
            self._put(f'"{prim_obj}"')
        elif _type == bool:
            val = "true" if prim_obj else "false"
            self._put(f'{val}')
        elif _type in (list, tuple):
            self._put('[')
            for i, obj in enumerate(prim_obj):
                if i != 0:
                    self._put(",")
                self._visit(obj)
            self._put(']')
        elif _type == bytes:
            encoded = prim_obj.hex()
            self._put(f'"{encoded}"')

    def _visit_list(self, obj: any, container_name: str):
        print(obj)
        pass

    def _visit_complex(self, comp_obj: any, container_name: str):
        self._push_name(container_name)
        name = self._get_concat_name()
        self._put(f'[{name}]\n')

        if type(comp_obj) == dict:
            self._visit_dict(comp_obj)
        elif type(comp_obj) == ModuleType:
            self._visit_module(comp_obj)
        elif inspect.isclass(comp_obj):
            self._visit_class(comp_obj)
        elif callable(comp_obj):
            self._visit_func(comp_obj)
        elif isinstance(comp_obj, object):
            self._visit_obj(comp_obj)

        self._pop_name()

    def _visit(self, obj, new_name: str = ""):
        if self._is_primitive_type(obj):
            self._visit_primitive(obj)
        elif type(obj) in (tuple, list):
            self._visit_list(obj, new_name)
        else:
            self._visit_complex(obj, new_name)
