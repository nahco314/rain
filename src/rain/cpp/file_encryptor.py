import re
from pathlib import Path

from rain.cpp.cpp_encryptor_base import CppEncryptor
from rain.cpp.numbers.f32 import F32Encryptor
from rain.cpp.numbers.f64 import F64Encryptor
from rain.cpp.numbers.u32 import U32Encryptor
from rain.cpp.numbers.u64 import U64Encryptor
from rain.cpp.token_noise.encryptor import TokenNoiseEncryptor
from rain.header import header


class CppFileEncryptor(CppEncryptor):
    def encrypt_file(self, source: str, output_path: Path) -> None:
        source = source.encode()
        for cls in (U32Encryptor, U64Encryptor, F32Encryptor, F64Encryptor):
            source = source.replace(f"#define {cls.macro_name}(x) (x)".encode(), b"")
            source = re.sub(
                rf"{cls.macro_name}\(([^)]*)\)".encode(),
                lambda x: cls().encrypt(x.group(1)),
                source,
            )

        source = re.sub(
            r"^// RAIN_START_ENCRYPT\n((.|\n)*?)^// RAIN_END_ENCRYPT".encode(),
            lambda x: TokenNoiseEncryptor().encrypt_tokens(x.group(1)),
            source,
            flags=re.MULTILINE,
        )

        cpp_header = (
            "".join(f"// {l}" for l in header.splitlines(keepends=True)) + "\n\n"
        )

        source = cpp_header.encode() + source

        with open(output_path, "wb") as f:
            f.write(source)
