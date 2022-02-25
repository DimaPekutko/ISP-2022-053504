import argparse
from utils import error_exit, get_file_ext
from libcore.serializer_table import SERIALIZERS

def _check_args(args: dict):
    # check invalid flags values
    if args["from"] is None or args["to"] is None:
        error_exit("Invalid --from or --to flag")
    # check invalid extensions
    ext1 = get_file_ext(args["from"])
    ext2 = get_file_ext(args["to"])
    if ext1 not in SERIALIZERS.keys() or ext2 not in SERIALIZERS.keys():
        error_exit(f"Invalid file exteinsion {ext1} -> {ext2}")
    if ext1 == ext2:
        exit()

def parse_file_paths() -> list:
    parser = argparse.ArgumentParser(description="Serializers:")
    parser.epilog = "Supported file types: ."+", .".join([ser for ser in SERIALIZERS.keys()])
    parser.add_argument("--from", dest="from", )
    parser.add_argument("--to", dest="to")
    args = parser.parse_args().__dict__
    _check_args(args)
    return [args["from"], args["to"]]
    