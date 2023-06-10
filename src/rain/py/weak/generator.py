from rain.generator import OneDataGenerator
from rain.generator import iter_bits


class WeakGenerator(OneDataGenerator):
    base = b"""\
# coding: raw_unicode_escape

# %s

crypto = "%s"
bits = []
for byte in crypto.encode()[1::2]:
    for i in range(6)[::-1]:
        bits.append((byte >> i) & 1)
bits = bits[:8 * (len(bits) // 8)]

source = bytearray()
for i in range(0, len(bits), 8):
    byte = 0
    for j in range(8):
        byte |= bits[i + j] << (7 - j)
    source.append(byte)

exec(source.decode("utf-8"))
"""

    @staticmethod
    def encrypt(string: str) -> bytes:
        code = string.encode()
        result_bits = []

        for bit in iter_bits(code):
            if len(result_bits) % 8 == 0:
                result_bits.extend((1, 0))

            result_bits.append(bit)

        while len(result_bits) % 8 != 0:
            result_bits.append(0)

        result = bytearray()
        for i in range(0, len(result_bits), 8):
            byte = 0
            for j in range(8):
                byte |= result_bits[i + j] << (7 - j)
            result.append(byte)

        return bytes(result)
