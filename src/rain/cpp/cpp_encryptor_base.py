from abc import ABC, abstractmethod

from rain.encryptor import Encryptor
from rain.common import e_display


class CppEncryptor(Encryptor, ABC):
    @property
    def true(self) -> bytes:
        return b"'%s'<'%s'" % (self.null, self.question)

    @property
    def false(self) -> bytes:
        return b"'%s'<'%s'" % (self.null, self.null)

    def bool(self, value: bool) -> bytes:
        if value:
            return self.true
        else:
            return self.false

    @property
    def if_true(self) -> bytes:
        return b"#if" + self.true + b"\n"

    @property
    def if_false(self) -> bytes:
        return b"#if" + self.false + b"\n"

    def if_bool(self, value: bool) -> bytes:
        if value:
            return self.if_true
        else:
            return self.if_false

    @property
    def end_if(self) -> bytes:
        return b"#endif\n"

    @property
    def display(self) -> bytes:
        return b"// " + e_display.encode() + b"\n\n"


class CppLiteralEncryptor(CppEncryptor, ABC):
    macro_name: str

    @abstractmethod
    def encrypt(self, string: bytes) -> bytes:
        raise NotImplementedError

    def build_error(self, item: bytes) -> ValueError:
        return ValueError(f"Invalid literal: {self.macro_name}({item.decode()})")
