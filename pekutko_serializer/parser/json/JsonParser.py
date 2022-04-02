import base64
import re
from types import CodeType, FunctionType
from pekutko_serializer.dto import DTO, DTO_TYPES
import pekutko_serializer.parser.json.json_tokens as JSON_TOKENS


class JsonParser():

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
            for token in JSON_TOKENS.JSON_TOKEN_REGEXPS.items():
                try:
                    regexp_res = re.match(token[1], source)
                    if regexp_res.start() == 0:
                        source = str(
                            source[regexp_res.end()-regexp_res.start():]).strip()
                        if token[0] == JSON_TOKENS.STR:
                            string = regexp_res.group(0)
                            tokens.append((token[0], string.replace('"', "")))
                        elif token[0] == JSON_TOKENS.NUMBER:
                            num = regexp_res.group(0)
                            num = float(num) if "." in num else int(num)
                            tokens.append((token[0], num))
                        else:
                            tokens.append((token[0],))
                except:
                    None
        return tokens

    def _skip_field_name(self, comma: bool = False) -> str:
        if comma:
            self._eat(JSON_TOKENS.COMMA)
        field_key = self._eat(JSON_TOKENS.STR)
        self._eat(JSON_TOKENS.COLON)
        return field_key[1]

    def _parse_func_code(self) -> CodeType:
        code_dict = self._parse()
        func_code = CodeType(
            int(code_dict["co_argcount"]),
            int(code_dict["co_posonlyargcount"]),
            int(code_dict["co_kwonlyargcount"]),
            int(code_dict["co_nlocals"]),
            int(code_dict["co_stacksize"]),
            int(code_dict["co_flags"]),
            bytes.fromhex(code_dict["co_code"]),
            tuple(code_dict["co_consts"]),
            tuple(code_dict["co_names"]),
            tuple(code_dict["co_varnames"]),
            str(code_dict["co_filename"]),
            str(code_dict["co_name"]),
            int(code_dict["co_firstlineno"]),
            bytes.fromhex(code_dict["co_lnotab"]),
            tuple(code_dict["co_freevars"]),
            tuple(code_dict["co_cellvars"]),
        )
        return func_code

    def _parse_func(self) -> any:
        # name
        self._skip_field_name()
        func_name = self._parse()
        # globals
        self._skip_field_name(comma=True)
        func_globals = self._parse()
        # code
        self._skip_field_name(comma=True)
        func_code = self._parse_func_code()

        func = FunctionType(func_code, func_globals, func_name)
        func.__globals__["__builtins__"] = __import__("builtins")
        return func

    def _parse_class(self) -> type:
        # name
        self._skip_field_name()
        class_name = self._parse()
        # fields
        self._skip_field_name(comma=True)
        class_members_dict = self._parse()

        _class = type(class_name, (object,), class_members_dict)
        return _class

    def _parse_obj(self) -> object:
        # class
        self._skip_field_name()
        _class = self._parse()
        # fields
        self._skip_field_name(comma=True)
        fields_dict = self._parse()

        obj = _class()
        obj.__dict__ = fields_dict
        return obj

    def _parse_dict(self):
        _dict = {}
        is_first = True
        while self._head_token()[0] != JSON_TOKENS.RBRACE:
            co_key = self._skip_field_name(not is_first)
            co_value = self._parse()
            _dict.update({co_key: co_value})
            is_first = False
        return _dict

    def _parse_list(self) -> list:
        self._skip_field_name()
        self._eat(JSON_TOKENS.LBRACKET)
        _list = []
        is_first = True
        while self._head_token()[0] != JSON_TOKENS.RBRACKET:
            # print(is_first)
            if not is_first:
                self._eat(JSON_TOKENS.COMMA)
            _list.append(self._parse())
            is_first = False
        self._eat(JSON_TOKENS.RBRACKET)
        return _list

    def _parse_primitive(self) -> any:
        token_type = self._head_token()[0]
        res = None
        if token_type == JSON_TOKENS.NUMBER:
            res = self._eat(JSON_TOKENS.NUMBER)[1]
        elif token_type == JSON_TOKENS.STR:
            res = self._eat(JSON_TOKENS.STR)[1]
        elif token_type in JSON_TOKENS.LBRACKET:
            res = self._parse_list()
        if self._head_token()[0] == JSON_TOKENS.COMMA:
            self._eat(JSON_TOKENS.COMMA)
        return res

    def _parse_dto(self):
        self._eat(JSON_TOKENS.LBRACE)

        if self._head_token()[0] == JSON_TOKENS.RBRACE:
            self._eat(JSON_TOKENS.RBRACE)
            return None

        dto_type_key = self._eat(JSON_TOKENS.STR)
        self._eat(JSON_TOKENS.COLON)
        dto_type_value = self._eat(JSON_TOKENS.STR)
        self._eat(JSON_TOKENS.COMMA)

        res_dto = None

        if dto_type_key[1] == DTO.dto_type:
            if dto_type_value[1] == DTO_TYPES.DICT:
                res_dto = self._parse_dict()
            elif dto_type_value[1] == DTO_TYPES.FUNC:
                res_dto = self._parse_func()
            elif dto_type_value[1] == DTO_TYPES.CLASS:
                res_dto = self._parse_class()
            elif dto_type_value[1] == DTO_TYPES.OBJ:
                res_dto = self._parse_obj()
        else:
            raise Exception(
                f"Field '{DTO.dto_type}' must be on top of the json object")

        self._eat(JSON_TOKENS.RBRACE)
        return res_dto

    def _parse(self) -> any:
        head_token_type = self._head_token()[0]
        if head_token_type == JSON_TOKENS.LBRACE:
            return self._parse_dto()
        return self._parse_primitive()

    def parse(self, s: str) -> any:
        self.__tokens = self._lex(s)
        return self._parse()
