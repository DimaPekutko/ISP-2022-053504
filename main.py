from pekutko_serializer import JsonSerializer

glob = 2

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

s = json_ser.dumps(test)

open("data.json", "w").write(s)
# exit()
# # exit()
res = json_ser.loads(s)
print(res())