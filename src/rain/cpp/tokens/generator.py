from pathlib import Path

from rain.cpp.prepro_generator_base import PreProcessorGenerator
from rain.cpp.tokenize import Tokenizer


class TokensGenerator(PreProcessorGenerator):
    def generate(self, source: str, output_path: Path) -> None:
        tokens = Tokenizer().tokenize(source)
        set_token = {t for t in tokens if not t.startswith("#")}

        result = bytearray()
        result.extend(self.display)

        for token in tokens:
            if token.startswith("#"):
                result.extend(token.encode())
            else:
                for ca in set_token:
                    if ca == token:
                        result.extend(self.if_true)
                    else:
                        result.extend(self.if_false)
                    result.extend(ca.encode())
                    result.extend(b"\n")
                    result.extend(self.end_if)

        with open(output_path, "wb") as f:
            f.write(result)
