import struct
from abc import ABC
from typing import Type, Literal

from rain.cpp.cpp_encryptor_base import CppLiteralEncryptor
from rain.cpp.numbers.uint import UIntEncryptor


class FloatEncryptor(CppLiteralEncryptor, ABC):
    as_uint_cls: Type[UIntEncryptor]
    type_name: str
    fmt_c: Literal["f", "d"]

    def encrypt(self, string: bytes) -> bytes:
        try:
            value = float(string)
        except ValueError:
            raise self.build_error(string)

        return self.encrypt_float(value)

    def encrypt_float(self, num: float) -> bytes:
        p = struct.pack(self.fmt_c, num)
        ib = int.from_bytes(p[::-1])

        res = f"bit_cast<{self.type_name}>(".encode()
        res += self.as_uint_cls().encrypt_uint(ib)
        res += b")"

        return res
