import re

from rain.cpp.cpp_encryptor_base import CppEncryptor, CppLiteralEncryptor
from rain.cpp.numbers.float import FloatEncryptor
from rain.cpp.numbers.u32 import U32Encryptor
from rain.cpp.numbers.u64 import U64Encryptor
from rain.cpp.numbers.uint import UIntEncryptor
from rain.encryptor import Encryptor


class F64Encryptor(FloatEncryptor):
    macro_name = "rain_encrypt_f64"
    as_uint_cls = U64Encryptor
    type_name = "double"
    fmt_c = "d"
