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
    b = "hello"


def test():
    a = mod_test.from_val
    b = some()
    return (2+glob+b)*a


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
print(res)
