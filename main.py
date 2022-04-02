import inspect
from pekutko_serializer import JsonSerializer

glob = 2

class TestClass():
    a = 32
    __dw__ = 2
    def __init__(self):
        pass

def test():
    print("hello")
    return 2+glob

json_ser = JsonSerializer()

# s = json_ser.dumps({
#     "a": 228,
#     "b": {
#         "c": 543
#     }
# })

obj = TestClass()
obj.a = 3
# print(obj)

s = json_ser.dumps(obj)

open("data.json", "w").write(s)
# exit()
# exit()
# # exit()
res = json_ser.loads(s)
print(res.a)