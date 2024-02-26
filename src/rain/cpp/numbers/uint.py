import re
from abc import ABC

from rain.cpp.cpp_encryptor_base import CppEncryptor, CppLiteralEncryptor
from rain.encryptor import Encryptor


class UIntEncryptor(CppLiteralEncryptor, ABC):
    bit_cnt: int
    prefix: str

    def encrypt(self, string: bytes) -> bytes:
        if not re.match(rb"\d+", string):
            raise self.build_error(string)
        return self.encrypt_uint(int(string))

    def encrypt_uint(self, num: int) -> bytes:
        res = b"0 + \n"
        for i in range(self.bit_cnt):
            res += self.if_bool((num >> i) & 1 == 1)
            res += f"{2 ** i}u{self.prefix} + \n".encode()
            res += self.end_if
        res += b"0"

        return res
