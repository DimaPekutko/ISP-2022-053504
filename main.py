from pekutko_serializer import JsonSerializer, TomlSerializer

import mod_test

from mod_test import from_val


glob = 2

def some():
    return 2


class TestClass():
    b = 28
    def __init__(self, c):
        self.b = c
        print(f"new {self.__class__.__name__} object")


def test(arg1):
    # a = mod_test.from_val
    # b = some()
    return (2+glob+2)*2


toml_ser = TomlSerializer()

test_dict = {
    "hello": 228,
    "a": {
        "b": 3,
        "c": "hello",
        "d": {
            "a": test
        }
    }
}

s = toml_ser.dumps(test_dict)

open("data.toml", "w").write(s)


# json_ser = JsonSerializer()
# obj = TestClass(c=228)
# obj.a = 3
# print(obj)
# s = json_ser.dumps(obj)
# open("data.json", "w").write(s)
# exit()
# exit()
# # exit()
# res = json_ser.loads(s)
# print(res.b)
