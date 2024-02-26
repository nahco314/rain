import re

from rain.cpp.cpp_encryptor_base import CppEncryptor, CppLiteralEncryptor
from rain.cpp.numbers.uint import UIntEncryptor
from rain.encryptor import Encryptor


class U64Encryptor(UIntEncryptor):
    macro_name = "rain_encrypt_u64"
    bit_cnt = 64
    prefix = "ll"
