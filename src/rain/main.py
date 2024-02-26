import argparse
from pathlib import Path

from rain.cpp.file_encryptor import CppFileEncryptor
from rain.cpp.numbers.u32 import U32Encryptor


def command_cpp(args):
    generator = CppFileEncryptor()

    with open(args.source, "r") as f:
        generator.encrypt_file(f.read(), Path(args.output))

    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    cpp_parser = subparsers.add_parser("cpp")

    cpp_parser.add_argument("source", type=str)
    cpp_parser.add_argument("output", type=str)
    cpp_parser.set_defaults(handler=command_cpp)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
