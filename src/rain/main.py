import argparse
from pathlib import Path

from rain.cpp.tokens.generator import TokensGenerator
from rain.generator import Generator
from rain.py.aes.generator import AESGenerator
from rain.py.embed.generator import EmbedGenerator
from rain.py.simple_embed.generator import SimpleEmbedGenerator
from rain.py.weak.generator import WeakGenerator

py_generator_name_map = {
    "aes": AESGenerator,
    "embed": EmbedGenerator,
    "se": SimpleEmbedGenerator,
    "weak": WeakGenerator,
}

cpp_generator_name_map = {
    "tokens": TokensGenerator,
}


def command_py(args):
    generator: Generator = py_generator_name_map[args.generator]()

    with open(args.source, "r") as f:
        generator.generate(f.read(), Path(args.output))

    print("Done.")


def command_cpp(args):
    generator: Generator = cpp_generator_name_map[args.generator]()

    with open(args.source, "r") as f:
        generator.generate(f.read(), Path(args.output))

    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    py_parser = subparsers.add_parser("py")

    py_parser.add_argument("source", type=str)
    py_parser.add_argument("output", type=str)
    py_parser.add_argument(
        "-g", "--generator", choices=py_generator_name_map.keys(), default="aes"
    )
    py_parser.set_defaults(handler=command_py)

    cpp_parser = subparsers.add_parser("cpp")

    cpp_parser.add_argument("source", type=str)
    cpp_parser.add_argument("output", type=str)
    cpp_parser.add_argument(
        "-g", "--generator", choices=cpp_generator_name_map.keys(), default="tokens"
    )
    cpp_parser.set_defaults(handler=command_cpp)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
