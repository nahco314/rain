from pathlib import Path

from rain.cpp.tokenize import Tokenizer
from rain.generator import Generator
from rain.cpp.prepro_generator_base import PreProcessorGenerator

from secrets import randbelow, choice


class TokenNoiseGenerator(PreProcessorGenerator):
    def generate(self, source: str, output_path: Path) -> None:
        tokens = Tokenizer().tokenize(source)

        all_tokens = [(tok, True) for tok in tokens]

        for _ in range(len(tokens) * 3):
            all_tokens.insert(randbelow(len(all_tokens)), (choice(tokens), False))

        result = bytearray()

        for token, is_true in all_tokens:
            if is_true:
                result.extend(self.if_true)
            else:
                result.extend(self.if_false)
            result.extend(token.encode())
            result.extend(b"\n")
            result.extend(self.end_if)

        with open(output_path, "wb") as f:
            f.write(result)
