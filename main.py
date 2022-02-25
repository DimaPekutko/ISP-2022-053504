from genericpath import isfile
import json
from ui import parse_file_paths
from utils import get_file_ext
from libcore import create_serializer
from libcore import Some

var = 3

class Some():
    def __init__(self):
        self.a = 3
        self.some = 33
    def r(self):
        self.a = 333
    def MET(self):
        return self.a + var

def main():
    [from_file_path, to_file_path] = parse_file_paths()
    # if isfile(from_file_path) and isfile(to_file_path):
    source_ser = create_serializer(get_file_ext(from_file_path))
    target_ser = create_serializer(get_file_ext(to_file_path))

    # a = 2
    s = source_ser.dumps(Some())
    
    with open ("data.json", "w") as file:
        file.write(s)

    obj = source_ser.loads(s)

    # print(s)

if __name__ == "__main__":
    main()