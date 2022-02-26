import inspect

JSON_SER_TYPES = {
    "class": "@CLASS",
    "function": "@FUNC",
    "object": "@OBJECT"
}

# _STR("}")
    # code = some_func.__code__
    # wtf = types.CodeType(
    #     code.co_argcount,
    #     code.co_posonlyargcount,
    #     code.co_kwonlyargcount,
    #     code.co_nlocals,
    #     code.co_stacksize,
    #     code.co_flags,
    #     bytes(code.co_code),
    #     code.co_consts,
    #     code.co_names,
    #     code.co_varnames,
    #     code.co_filename,
    #     "my_test",
    #     code.co_firstlineno,
    #     code.co_lnotab,
    #     code.co_freevars,
    #     code.co_cellvars
    # )
    # my_func = types.FunctionType(wtf, some_func.__globals__, "my_test")
    # print(my_func(2,3))

_result_str = ""

def _visit_class(obj):
    user_members, sys_members = [], []
    if obj.__init__.__class__.__name__ == "function":
        user_members.append(("__init__", obj.__init__))
    for mem in obj.__dict__.items():
        if not str(mem[0]).startswith("__"):
            user_members.append(mem)
        else:
            sys_members.append(mem)
    # filling class fields 
    _STR(f'"{JSON_SER_TYPES["class"]}":'+"{")
    _STR(f'"@name":"{obj.__name__}",')
    _STR(f'"@dict":'+"{")
    for i in range(len(user_members)):
        name = user_members[i][0]
        value = user_members[i][1]
        _STR(f'"{name}":')
        if callable(value):
            _STR("{")
            _visit(value)
            _STR("}")
        else:
            _visit(value)
        if i+1 != len(user_members):
            _STR(f",")
    _STR("} }")

def _visit_function(obj):
    assert callable(obj)
    func_name = obj.__name__
    func_code_settings = dict(inspect.getmembers(obj.__code__))
    func_globals = {}
    # filling function global vars list (need for dynamic object generation)
    for glob_var in obj.__globals__.items():
        if glob_var[0] in func_code_settings["co_names"]:
            func_globals.update({glob_var[0]: glob_var[1]})
    # print(func_globals)
    # generating output code
    _STR(f'"{JSON_SER_TYPES["function"]}":'+"{")
    _STR(f'"@name":"{func_name}",')
    # filling global vars
    _STR(f'"@globals":'+"{")
    _visit(func_globals)
    _STR("},")
    co_fields = list(func_code_settings.items())
    co_fields = [field for field in co_fields if field[0].startswith("co_")]
    # filling code settings 
    for i in range(len(co_fields)):
        field_name = co_fields[i][0]
        field_value = co_fields[i][1]            
        _STR(f'"{field_name}":')
        _visit(field_value)
        if i+1 != len(co_fields):
            _STR(f",")
    _STR("}")

def _visit_obj(obj):
    obj_class = obj.__class__
    obj_dict = obj.__dict__
    _STR(f'"{JSON_SER_TYPES["object"]}":'+"{")
    _visit(obj_class)
    _STR(f',"@dict":'+"{")
    _visit(obj_dict)
    _STR("} }")
    pass    

def _visit(obj: any):
    _type = type(obj)
    if obj is None:
        _STR("null")
    # class case
    elif inspect.isclass(obj):
        _visit_class(obj)
    # function case
    elif callable(obj):
        _visit_function(obj)
    # primitive types case
    elif _type in (int, float):
        _STR(f"{obj}")
    elif _type is str:
        _STR(f'"{obj}"')
    elif _type is dict:
        items = list(obj.items())
        for i in range(len(items)):
            _STR(f'"{items[i][0]}":')
            _visit(items[i][1])
            if i+1 != len(items):
                _STR(f",")
    elif _type in (tuple, list, set):
        _STR(f"[")
        for i in range(len(obj)):
            if not inspect.isclass(obj[i]):
                _visit(obj[i])
                if i+1 != len(obj):
                    _STR(f",")
        _STR(f"]")
    elif _type in (bytes, bytearray):
        _STR(f'{list(bytes(obj))}')
    # object case
    elif not isinstance(obj, (int, float, bool, str, list, tuple, dict)):
        _visit_obj(obj)
 
def _STR(s: str):
    global _result_str
    _result_str += s

def serialize(obj: any):
    _STR("{")
    _visit(obj)
    _STR("}")
    return _result_str