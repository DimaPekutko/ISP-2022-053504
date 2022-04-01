import base64
import inspect
from ..BaseSerializer import BaseSerializer
from pekutko_serializer.dto import DTO, DTO_TYPES

class JsonSerializer(BaseSerializer):
    __res_str = ""
    
    def dumps(self, obj: any) -> str:
        self.__res_str = ""
        self._visit(obj)
        return self.__res_str
    def dump(self, obj: any, file_path: str):
        pass
    def loads(self, source: str) -> any:
        pass
    def load(self, file_path: str) -> any:
        pass

    def _put(self, s: str):
        self.__res_str += s

    def _visit_func_globals(self, func):
        self._put('{')
        code = func.__code__
        func_globals = func.__globals__.items()
        is_first_item = True
        for glob in func_globals:
            if glob[0] in code.co_names:
                if not is_first_item:
                    self._put(',')
                self._put(f'"{glob[0]}": ')
                self._visit(glob[1])
                is_first_item = False
        self._put('}')

    def _visit_func_code(self, func):
        self._put('{')
        code = func.__code__
        is_first_item = True
        for member in inspect.getmembers(code):
            if str(member[0]).startswith("co_"):
                if not is_first_item:
                    self._put(',')
                self._put(f'"{member[0]}":')
                self._visit(member[1])
                is_first_item = False
        self._put('}')

    def _visit_func(self, func):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.FUNC}",')
        self._put(f'"{DTO.name}": "{func.__name__}",')
        self._put(f'"{DTO.global_names}": ')
        self._visit_func_globals(func)
        self._put(',')
        self._put(f'"{DTO.code}": ')
        self._visit_func_code(func)
        # self._put(',')

    def _visit_literal(self, literal):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.LITERAL}",')
        if type(literal) == str:
            self._put(f'"{DTO.value}": "{literal}"')
        elif type(literal) == bytes:
            encoded = base64.b64encode(literal)
            self._put(f'"{DTO.value}": "{encoded}"')
        else:
            self._put(f'"{DTO.value}": {literal}')

    def _visit_tuple(self, tuple_obj):
        self._put(f'"{DTO.dto_type}": "{DTO_TYPES.TUPLE}",')
        self._put(f'"{DTO.value}": ')
        self._put('[')
        for i, obj in enumerate(tuple_obj):
            if i != 0:
                self._put(",")
            self._visit(obj)
        self._put(']')

    def _visit(self, obj):
        self._put("{")

        if type(obj) in (int, float, str, bool, bytes):
            self._visit_literal(obj)
        elif type(obj) == tuple:
            self._visit_tuple(obj)
        elif callable(obj):
            self._visit_func(obj)

        self._put("}")