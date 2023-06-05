import base64
import secrets
import shutil
import subprocess
from pathlib import Path
from tempfile import mkstemp
from typing import Optional

from rain.generator import Generator
from rain.generator import iter_bits


class AESGenerator(Generator):
    base = b"""\
# coding: raw_unicode_escape

import subprocess
import base64


key = base64.b64encode("%(key)s".encode())

with open("./data", "w+") as f:
    subprocess.run(f"openssl enc -d -aes-256-cbc -pbkdf2 -k {key}".split(), input=base64.b64decode("%(crypto)s"), stdout=f)
    f.seek(0)
    source = f.read()

exec(source)
"""

    def encrypt_aes(self, key: bytes, data: str):
        data_file: Optional[Path] = None
        crypto_file: Optional[Path] = None
        try:
            data_file = Path(mkstemp()[1])
            crypto_file = Path(mkstemp()[1])
            with open(data_file, "w") as f:
                f.write(data)
            conv_key = base64.b64encode(self.as_inner_question(key))
            subprocess.run(
                [
                    "openssl",
                    "enc",
                    "-e",
                    "-aes-256-cbc",
                    "-pbkdf2",
                    "-k",
                    str(conv_key),
                    "-in",
                    str(data_file),
                    "-out",
                    str(crypto_file),
                ]
            )
            shutil.copy(crypto_file, Path("./crypto_b"))
            with open(crypto_file, "rb") as f:
                return f.read()
        finally:
            if data_file is not None:
                data_file.unlink()
            if crypto_file is not None:
                crypto_file.unlink()

    def _gen_key(self) -> bytes:
        result = bytearray()

        bytes_ = secrets.token_hex(256 // 8).encode()
        for bit in iter_bits(bytes_):
            if bit == 0:
                result.extend(self.null)
            else:
                result.extend(self.question)

        return bytes(result)

    def generate(self, source: str, output_path: Path) -> None:
        key = self._gen_key()
        crypto = base64.b64encode(self.encrypt_aes(key, source))

        result = self.base % {b"key": key, b"crypto": crypto}

        with open(output_path, "wb") as f:
            f.write(result)
