from rain.generator import OneDataGenerator
from rain.generator import iter_bits


class EmbedGenerator(OneDataGenerator):
    base = base = b"""\
# coding: raw_unicode_escape

crypto = "%s"
code = crypto.encode()
bits = []
i = 0
while i < len(code):
    if code[i] == 0:
        bits.append(0)
        i += 1
    else:
        bits.append(1)
        i += 6

source = bytearray()
for i in range(0, len(bits), 8):
    byte = 0
    for j in range(8):
        byte |= bits[i + j] << (7 - j)
    source.append(byte)

exec(source.decode("utf-8"))
"""

    def encrypt(self, string: str) -> bytes:
        code = string.encode()
        bits = list(iter_bits(code))

        result = bytearray()

        for bit in bits:
            if bit == 0:
                result.extend(self.null)
            else:
                result.extend(self.question)

        return bytes(result)
