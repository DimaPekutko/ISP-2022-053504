import inspect
from types import BuiltinFunctionType, GetSetDescriptorType, MappingProxyType, MethodDescriptorType, WrapperDescriptorType
from ..BaseSerializer import BaseSerializer
from pekutko_serializer.parser.json.JsonParser import JsonParser
from pekutko_serializer.dto import DTO, DTO_TYPES


class JsonSerializer(BaseSerializer):
    __res_str = ""
    __parser = None

    def __init__(self):
        super().__init__()
        self.__parser = JsonParser()

    def dumps(self, obj: any) -> str:
        self.__res_str = ""
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

    def _visit_func_globals(self, func):
        code = func.__code__
        func_globals = func.__globals__.items()
        actual_globals = {}
        for glob in func_globals:
            if glob[0] in code.co_names:
                actual_globals.update({glob[0]: glob[1]})
        self._visit(actual_globals)

    def _visit_func_code(self, func):
        code = func.__code__
        code_dict = {}
        for member in inspect.getmembers(code):
            if str(member[0]).startswith("co_"):
                code_dict.update({member[0]: member[1]})
        self._visit(code_dict)

    def _visit_func(self, func):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.FUNC}",')
        self._put(f'"{DTO.name}": "{func.__name__}",')
        self._put(f'"{DTO.global_names}": ')
        self._visit_func_globals(func)
        self._put(',')
        self._put(f'"{DTO.code}": ')
        self._visit_func_code(func)

    def _visit_class(self, _class):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.CLASS}",')
        self._put(f'"{DTO.name}": "{_class.__name__}",')
        self._put(f'"{DTO.fields}": ')
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
                    fields_dict.update({mem[0]:mem[1]})
        self._visit(fields_dict)

    def _visit_dict(self, _dict: dict):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.DICT}"')
        if len(_dict.items()) >= 1:
            self._put(",")
        is_first = True
        for item in _dict.items():
            if not is_first:
                self._put(',')
            self._put(f'"{item[0]}": ')
            self._visit(item[1])
            is_first = False

    def _visit_primitive(self, prim_obj):
        _type = type(prim_obj)
        if _type in (int, float):
            self._put(f'{prim_obj}')
        elif _type == str:
            self._put(f'"{prim_obj}"')
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

    def _visit(self, obj):
        if type(obj) in (int, float, str, bool, bytes, tuple, list):
            self._visit_primitive(obj)
        elif obj == None:
            self._put('{}')
        else:
            self._put('{')
            if type(obj) == dict:
                self._visit_dict(obj)
            elif inspect.isclass(obj):
                self._visit_class(obj)
            elif callable(obj):
                self._visit_func(obj)
            self._put('}')