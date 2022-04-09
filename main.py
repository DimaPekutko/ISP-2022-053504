import inspect
import types
import yaml
import toml
import json
from pekutko_serializer import JsonSerializer, TomlSerializer, YamlSerializer, utils

import mod_test
import sys

from mod_test import from_val

import math

glob = 2


def some():
    return 2


class TestClass():
    b = 28

    def __init__(self):
        pass


def test(arg1):
    # a = math.pi
    # a = mod_test.from_val
    # b = some()
    return (2+glob+2)*2

test_dict = {
    "a": 228,
    "b": [2,3],
    "c": {
        "d": "hello",
        "b": True
    },
}

def closure228():
    def insome():
        return 2

    return insome

class Meta228(type):
    s = 33
    def __new__(cls, name, bases, dct):
        print("ya")
        return type(name, bases,dct)

# class Some(metaclass=Meta228):
#     pass

# for m in inspect.getmembers(Some):
#     print(m)

# f = inspect.getmembers(closure228)
# for r in f:
    # print(r)
# exit()

class TestClass():
    some_bool_value = True
    class_value = 18
    c = 10.2

    def __init__(self, a: int, b: int = 2):
        self.c += (a+b)

    def count(self) -> int:
        return self.c/18

class ccc(metaclass=Meta228):
    pass

# print([2,3,4][:-1], [2,3,4][-1:])

obj = test

toml_ser = TomlSerializer()
json_ser = JsonSerializer()
yaml_ser = YamlSerializer()

s1 = json_ser.dumps(obj)
s2 = toml_ser.dumps(obj)
s3 = yaml_ser.dumps(obj)

open("data.json", "w").write(s1)
open("data.toml", "w").write(s2)
open("data.yaml", "w").write(s3)

# g = 228


res1 = json_ser.loads(s1)
res2 = toml_ser.loads(s2)
res3 = yaml_ser.loads(s3)
# print("_____MAIN_____")

print(res1(2))
print(res2(2))
print(res3(2))

# print()
# print("JSON")
# print()
# # for m in inspect.getmembers(res1.__code__):
# #     print(m)

# print()
# print("TOML")
# print()
# # for m in inspect.getmembers(res2.__code__):
# #     print(m)
# # res = yaml_ser.loads(s3)
# # res2.__code__["co_consts"] = res1.__code__.co_consts
# # setattr(res2.__code__, "co_consts", res1.__code__.co_consts)
# print(res2())

# res = json_ser.loads(s2)
# print(res2())

# json_ser = JsonSerializer()
# obj = TestClass(c=228)
# obj.a = 3
# print(obj)
# exit()
# exit()
# # exit()
# res = json_ser.loads(s2)
# print(res.b)
