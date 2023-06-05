from rain.generator import OneDataGenerator
from rain.generator import iter_bits


class SimpleEmbedGenerator(OneDataGenerator):
    base = base = b"""\
# coding:raw_unicode_escape
exec(bytes.fromhex(hex(sum([2**i*(x>0)for i,x in enumerate("%s".encode()[::-6])]))[3:]).decode())\
"""

    def encrypt(self, string: str) -> bytes:
        code = string.encode()
        bits = list(iter_bits(code))

        result = bytearray()

        for bit in bits:
            if bit == 0:
                result.extend(self.null * 6)
            else:
                result.extend(self.question)

        result.insert(0, 0xFF)

        return bytes(result)
