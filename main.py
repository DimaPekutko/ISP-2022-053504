from genericpath import isfile
from ui import parse_file_paths
from utils import get_file_ext
from libcore import create_serializer

def main():
    [from_file_path, to_file_path] = parse_file_paths()
    # if isfile(from_file_path) and isfile(to_file_path):
    ser1 = create_serializer(get_file_ext(from_file_path))
    ser2 = create_serializer(get_file_ext(to_file_path))
    print(ser1, ser2)

if __name__ == "__main__":
    main()

    # members = getmembers(some())
    # for mem in members:
    #     if not mem[0].startswith("__"):
    #         if type(mem[1]) is not str: 
    #             print(mem[1])