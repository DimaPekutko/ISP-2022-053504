from pekutko_serializer import JsonSerializer

import mod_test

from mod_test import from_val

glob = 2


def some():
    return 2


def factorial(n: int) -> int:
    if n <= 1:
        return 1
    else:
        return n*factorial(n-1)


class TestClass():
    b = 28
    def __init__(self, c):
        self.b = c
        print(f"new {self.__class__.__name__} object")


def test(arg1):
    # a = mod_test.from_val
    # b = some()
    return (2+glob+2)*2


json_ser = JsonSerializer()

obj = TestClass(c=228)
# obj.a = 3

# print(obj)
s = json_ser.dumps(obj)
open("data.json", "w").write(s)
# exit()
# exit()
# # exit()
res = json_ser.loads(s)
print(res.b)
