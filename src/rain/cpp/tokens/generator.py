from pathlib import Path

from rain.cpp.tokens.tokenize import Tokenizer
from rain.generator import Generator


class TokensGenerator(Generator):
    def generate(self, source: str, output_path: Path) -> None:
        tokens = Tokenizer().tokenize(source)
        set_token = {t for t in tokens if not t.startswith("#")}

        result = bytearray()

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

    @property
    def if_true(self) -> bytes:
        return b"#if '%s' == '%s'\n" % (self.null, self.null)

    @property
    def if_false(self) -> bytes:
        return b"#if '%s' == '%s'\n" % (self.null, self.question)

    @property
    def end_if(self) -> bytes:
        return b"#endif\n"
