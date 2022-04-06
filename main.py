import inspect
import yaml
import toml
import json
from pekutko_serializer import JsonSerializer, TomlSerializer, YamlSerializer

import mod_test

from mod_test import from_val


glob = 2


def some():
    return 2


class TestClass():
    b = 28

    def __init__(self, c):
        self.b = c
        a = 3
        print(f"new {self.__class__.__name__} object")


def test(arg1):
    # a = mod_test.from_val
    # b = some()
    return (2+glob+2)*2


toml_ser = TomlSerializer()
json_ser = JsonSerializer()
yaml_ser = YamlSerializer()

test_dict = {
    "a": 228,
    "b": {
        "c": 3,
        "d": "hello",
        "e": True
    },
    "f": {
        "hello": 2,
        "some": 3.14
    }
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

class ccc(metaclass=Meta228):
    pass

obj = Meta228

# s = toml_ser.dumps(obj)
s2 = json_ser.dumps(obj)
# s3 = yaml_ser.dumps(obj)

# open("data.yaml", "w").write(s3)
# open("data.toml", "w").write(toml.dumps(obj))
open("data.json", "w").write(s2)

# res = yaml_ser.loads(s2)

res = json_ser.loads(s2)
print(res)


# json_ser = JsonSerializer()
# obj = TestClass(c=228)
# obj.a = 3
# print(obj)
# exit()
# exit()
# # exit()
# res = json_ser.loads(s2)
# print(res.b)
