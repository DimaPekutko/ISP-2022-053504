import inspect
from pekutko_serializer import JsonSerializer

import mod_test

from mod_test import from_val

glob = 2


def some():
    return 2


class TestClass():
    a = mod_test.from_val
    __dw__ = 2

    def __init__(self):
        pass


def test():
    a = mod_test.from_val
    b = some()
    q = a + b
    d = mod_test.from_module("hey")
    c = 32
    r = mod_test.glob
    r += q
    return 2+glob+r


json_ser = JsonSerializer()

obj = TestClass()
# obj.a = 3

# print(obj)
s = json_ser.dumps(test)
open("data.json", "w").write(s)
# exit()
# exit()
# # exit()
res = json_ser.loads(s)
print(res())
