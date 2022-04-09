import argparse
import os
import sys

from numpy import source

from pekutko_serializer.serializer import create_serializer

class CLI:
    __parser = None

    def parse_args(self):
        self.__parser = argparse.ArgumentParser(
            description='Dmitry Pekutko formats serializer'
        )
        self.__parser.add_argument(
            "--source", type=str, help="File path to parse"
        )
        self.__parser.add_argument(
            "--to", type=str, help="File path to write"
        )
        self.__parser.add_argument(
            "--conf", type=str, help="Ignore args and use config file with path"
        )
        return self.__parser.parse_args()

    def exec_convert(self, cli_args):
        if cli_args.conf:
            pass
        else:
            source_path, to_path = cli_args.source, cli_args.to
            if source_path and to_path:
                if os.path.exists(source_path) and os.path.isfile(source_path):
                    cwd = os.getcwd()
                    # run convert with absolute paths
                    abs_source_path = os.path.join(cwd,str(source_path).strip())
                    abs_to_path = os.path.join(cwd,str(to_path).strip())
                    self.__convert(abs_source_path, abs_to_path)
                else:
                    self.__parser.error(f'No such file: "{source_path}"')
            else:
                self.__parser.error(
                    f'Invalid --source and --to flags: source="{source_path}", to="{to_path}"')

    def __convert(self, source_file_path: str, to_file_path: str):
        source_format = os.path.splitext(source_file_path)[1][1:]
        to_format = os.path.splitext(to_file_path)[1][1:]
        if source_format != to_format:
            source_ser = create_serializer(source_format)
            to_ser = create_serializer(to_format)
            if source_ser and to_ser:
                obj = source_ser.load(source_file_path)
                to_ser.dump(obj, to_file_path)
        else:
            print('Identic formats, exit.')
