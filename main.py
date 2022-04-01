from pekutko_serializer import JsonSerializer

def test():
    return 2

json_ser = JsonSerializer()

s = json_ser.dumps(test)

open("data.json", "w").write(s)