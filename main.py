import inspect
from pekutko_serializer import JsonSerializer

glob = 2

class TestClass():
    a = 32
    __dw__ = 2
    def __init__(self):
        print(self.a, self.__dw__)

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

s = json_ser.dumps(TestClass)

open("data.json", "w").write(s)
# exit()
# exit()
# # exit()
res = json_ser.loads(s)
print(res())