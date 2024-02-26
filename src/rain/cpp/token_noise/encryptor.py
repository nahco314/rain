from pathlib import Path
from secrets import choice
from secrets import randbelow

from rain.cpp.cpp_encryptor_base import CppEncryptor
from rain.cpp.tokenize import Tokenizer


class TokenNoiseEncryptor(CppEncryptor):
    def encrypt_tokens(self, source: bytes) -> bytes:
        tokens = Tokenizer().tokenize_1k(source)
        set_token = {t for t in tokens if not t.startswith(b"#")}

        all_tokens = [(tok, True) for tok in tokens]

        for _ in range(len(tokens) * 3):
            all_tokens.insert(
                randbelow(len(all_tokens)), (choice(list(set_token)), False)
            )

        result = bytearray()

        for token, is_true in all_tokens:
            if token.startswith(b"#"):
                result.extend(token)
                result.extend(b"\n")
                continue

            if is_true:
                result.extend(self.if_true)
            else:
                result.extend(self.if_false)
            result.extend(token)
            result.extend(b"\n")
            result.extend(self.end_if)

        return result
