import imp
import inspect
import re
from types import CodeType, FunctionType, ModuleType

from pekutko_serializer.dto import DTO, DTO_TYPES
import pekutko_serializer.parser.yaml.yaml_tokens as TOKEN_TYPES


class YamlParser():

    __tokens: list = []

    def _eat(self, token_types: tuple) -> tuple:
        if len(self.__tokens):
            if self.__tokens[0][0] in token_types:
                return self.__tokens.pop(0)
        return ("", "")

    def _head_token(self) -> tuple:
        if len(self.__tokens):
            return self.__tokens[0]

    def _lex(self, source: str) -> list:
        tokens = []
        while len(source) > 0:
            for token in TOKEN_TYPES.TOKEN_REGEXPS.items():
                if token[0] == TOKEN_TYPES.EOF:
                    continue
                regexp_res = re.match(token[1], source)
                if regexp_res and regexp_res.start() == 0 and len(regexp_res.group(0)):
                    source = str(
                        source[regexp_res.end()-regexp_res.start():])
                    if token[0] in (TOKEN_TYPES.STR, TOKEN_TYPES.FIELD_STR):
                        string = regexp_res.group(0)
                        tokens.append((token[0], string.replace('"', "")))
                    elif token[0] == TOKEN_TYPES.NUMBER:
                        num = regexp_res.group(0)
                        num = float(num) if "." in num else int(num)
                        tokens.append((token[0], num))
                    elif token[0] == TOKEN_TYPES.BOOL:
                        _bool = regexp_res.group(0)
                        res = True if _bool == "true" else False
                        tokens.append((token[0], res))
                    else:
                        tokens.append((token[0],))
        tokens.append((TOKEN_TYPES.EOF,))
        return tokens

    def _skip_field_name(self) -> str:
        while self._head_token()[0] == TOKEN_TYPES.GAP:
            self._eat(TOKEN_TYPES.GAP)
        field_key = self._eat(TOKEN_TYPES.FIELD_STR)
        self._eat(TOKEN_TYPES.COLON)
        return field_key[1]

    # def _parse_func_code(self) -> CodeType:
    #     code_dict = self._parse()
    #     func_code = CodeType(
    #         int(code_dict["co_argcount"]),
    #         int(code_dict["co_posonlyargcount"]),
    #         int(code_dict["co_kwonlyargcount"]),
    #         int(code_dict["co_nlocals"]),
    #         int(code_dict["co_stacksize"]),
    #         int(code_dict["co_flags"]),
    #         bytes.fromhex(code_dict["co_code"]),
    #         tuple(code_dict["co_consts"]),
    #         tuple(code_dict["co_names"]),
    #         tuple(code_dict["co_varnames"]),
    #         str(code_dict["co_filename"]),
    #         str(code_dict["co_name"]),
    #         int(code_dict["co_firstlineno"]),
    #         bytes.fromhex(code_dict["co_lnotab"]),
    #         tuple(code_dict["co_freevars"]),
    #         tuple(code_dict["co_cellvars"]),
    #     )
    #     return func_code

    # def _parse_func(self) -> any:
    #     # name
    #     self._skip_field_name()
    #     func_name = self._parse()
    #     # globals
    #     self._skip_field_name(comma=True)
    #     func_globals = self._parse()
    #     # exit()
    #     # code
    #     self._skip_field_name(comma=True)
    #     func_code = self._parse_func_code()

    #     func = FunctionType(func_code, func_globals, func_name)
    #     func.__globals__["__builtins__"] = __import__("builtins")
    #     return func

    # def _parse_module(self) -> ModuleType:
    #     # name
    #     self._skip_field_name()
    #     module_name = self._parse()
    #     # fields
    #     self._skip_field_name(comma=True)
    #     module_fields = self._parse()

    #     module = imp.new_module(module_name)
    #     # module["__dict__"] = module_fields
    #     for field in module_fields.items():
    #         setattr(module,field[0],field[1])
    #     return module

    # def _parse_class(self) -> type:
    #     # name
    #     self._skip_field_name()
    #     class_name = self._parse()
    #     # fields
    #     self._skip_field_name(comma=True)
    #     class_members_dict = self._parse()

    #     _class = type(class_name, (object,), class_members_dict)
    #     return _class

    # def _parse_obj(self) -> object:
    #     # class
    #     self._skip_field_name()
    #     _class = self._parse()
    #     # fields
    #     self._skip_field_name(comma=True)
    #     fields_dict = self._parse()

    #     class_init = _class.__init__
    #     if callable(class_init):
    #         if class_init.__class__.__name__ == "function":
    #             delattr(_class, "__init__")
    #     obj = _class()
    #     obj.__init__ = class_init
    #     obj.__dict__ = fields_dict
    #     return obj

    def _parse_dict(self):
        _dict = {}
        while self._head_token()[0] != TOKEN_TYPES.EOF:
            co_key = self._skip_field_name()
            self._eat(TOKEN_TYPES.NEW_LINE)
            co_value = self._parse()
            _dict.update({co_key: co_value})
        return _dict

    # def _parse_list(self) -> list:
    #     self._skip_field_name()
    #     self._eat(TOKEN_TYPES.LBRACKET)
    #     _list = []
    #     is_first = True
    #     while self._head_token()[0] != TOKEN_TYPES.RBRACKET:
    #         # print(is_first)
    #         if not is_first:
    #             self._eat(TOKEN_TYPES.COMMA)
    #         _list.append(self._parse())
    #         is_first = False
    #     self._eat(TOKEN_TYPES.RBRACKET)
    #     return _list

    def _parse_primitive(self) -> any:
        token_type = self._head_token()[0]
        res = None
        if token_type == TOKEN_TYPES.NUMBER:
            res = self._eat(TOKEN_TYPES.NUMBER)[1]
        elif token_type == TOKEN_TYPES.STR:
            res = self._eat(TOKEN_TYPES.STR)[1]
        elif token_type == TOKEN_TYPES.BOOL:
            res = self._eat(TOKEN_TYPES.BOOL)[1]
        elif token_type in TOKEN_TYPES.LBRACKET:
            res = self._parse_list()
        self._eat(TOKEN_TYPES.NEW_LINE)
        return res

    def _parse_dto(self):

        dto_type_key = self._eat(TOKEN_TYPES.FIELD_STR)
        self._eat(TOKEN_TYPES.COLON)
        dto_type_value = self._eat(TOKEN_TYPES.STR)
        self._eat(TOKEN_TYPES.NEW_LINE)

        res_dto = None

        if dto_type_key[1] == DTO.dto_type:
            if dto_type_value[1] == DTO_TYPES.DICT:
                res_dto = self._parse_dict()
            elif dto_type_value[1] == DTO_TYPES.FUNC:
                res_dto = self._parse_func()
            elif dto_type_value[1] == DTO_TYPES.MODULE:
                res_dto = self._parse_module()
    #         elif dto_type_value[1] == DTO_TYPES.CLASS:
    #             res_dto = self._parse_class()
    #         elif dto_type_value[1] == DTO_TYPES.OBJ:
    #             res_dto = self._parse_obj()
    #     else:
    #         raise Exception(
    #             f"Field '{DTO.dto_type}' must be on top of the json object")

    #     self._eat(TOKEN_TYPES.RBRACE)
        return res_dto

    def _parse(self) -> any:
        head_token_type = self._head_token()[0]
        if head_token_type == TOKEN_TYPES.FIELD_STR:
            return self._parse_dto()
        return self._parse_primitive()

    def parse(self, s: str) -> any:
        self.__tokens = self._lex(s)
        # remove all gaps
        self.__tokens = list(filter(
            lambda token: token[0] != TOKEN_TYPES.GAP,
            self.__tokens
        ))
        # for t in self.__tokens:
        #     print(t)
        #     pass
        # print(self.__tokens)
        return self._parse()
