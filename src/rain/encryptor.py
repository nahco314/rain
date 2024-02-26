from abc import abstractmethod, ABC
from pathlib import Path
from typing import Generator

from rain.common import e_display


def iter_bits(bytes_: bytes) -> Generator[int, None, None]:
    for byte in bytes_:
        for i in range(8)[::-1]:
            yield (byte >> i) & 1


class Encryptor(ABC):
    @property
    def null(self) -> bytes:
        return b"\x00"

    @property
    def question(self) -> bytes:
        return b"\xef\xbf\xbd"

    def as_inner_question(self, data: bytes) -> bytes:
        return (
            data.replace(b"\xef", b"\xc3\xaf")
            .replace(b"\xbf", b"\xc2\xbf")
            .replace(b"\xbd", b"\xc2\xbd")
        )
