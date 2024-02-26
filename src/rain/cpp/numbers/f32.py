import re

from rain.cpp.cpp_encryptor_base import CppEncryptor, CppLiteralEncryptor
from rain.cpp.numbers.float import FloatEncryptor
from rain.cpp.numbers.u32 import U32Encryptor
from rain.cpp.numbers.uint import UIntEncryptor
from rain.encryptor import Encryptor


class F32Encryptor(FloatEncryptor):
    macro_name = "rain_encrypt_f32"
    as_uint_cls = U32Encryptor
    type_name = "float"
    fmt_c = "f"
