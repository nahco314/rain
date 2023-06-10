from pathlib import Path
from secrets import choice
from secrets import randbelow

from rain.cpp.prepro_generator_base import PreProcessorGenerator
from rain.cpp.tokenize import Tokenizer


class TokenNoiseGenerator(PreProcessorGenerator):
    def generate(self, source: str, output_path: Path) -> None:
        tokens = Tokenizer().tokenize_1k(source)
        set_token = {t for t in tokens if not t.startswith("#")}

        all_tokens = [(tok, True) for tok in tokens]

        for _ in range(len(tokens) * 3):
            all_tokens.insert(
                randbelow(len(all_tokens)), (choice(list(set_token)), False)
            )

        result = bytearray()
        result.extend(self.display)

        for token, is_true in all_tokens:
            if token.startswith("#"):
                result.extend(token.encode())
                result.extend(b"\n")
                continue

            if is_true:
                result.extend(self.if_true)
            else:
                result.extend(self.if_false)
            result.extend(token.encode())
            result.extend(b"\n")
            result.extend(self.end_if)

        with open(output_path, "wb") as f:
            f.write(result)
