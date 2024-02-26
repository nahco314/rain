import re

from rain.cpp.cpp_encryptor_base import CppEncryptor, CppLiteralEncryptor
from rain.cpp.numbers.uint import UIntEncryptor
from rain.encryptor import Encryptor


class U32Encryptor(UIntEncryptor):
    macro_name = "rain_encrypt_u32"
    bit_cnt = 32
    prefix = "l"
