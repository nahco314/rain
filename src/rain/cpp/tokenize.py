import re
import secrets


class Tokenizer:
    preprocessor_directive = re.compile(rb"^#.*$", re.MULTILINE)
    comment = re.compile(rb"(//[^\n]*?$)|(/\*.*?\*/)", re.DOTALL | re.MULTILINE)

    name = re.compile(rb"[a-zA-Z_][a-zA-Z0-9_]*")  # keyword, identifier

    pointfloat = re.compile(rb"\d('?\d)*\.(\d('?\d)*)?([eE]-?\d('?\d)*)?[fFlL]?")
    intfloat = re.compile(rb"\d('?\d)*[eE]-?\d('?\d)*[fFlL]?")

    bin_int = re.compile(rb"0[bB][01]('?[01])*[uU]?[lL]{0,2}")
    hex_int = re.compile(rb"0[xX][0-9a-fA-F]('?[0-9a-fA-F])*[uU]?[lL]{0,2}")
    oct_int = re.compile(rb"0('?[0-7])*[uU]?[lL]{0,2}")
    int = re.compile(rb"\d('?\d)*[uU]?[lL]{0,2}")

    bool = re.compile(rb"(true|false)")

    char = re.compile(rb"(u8|L|u|U)?'(.|\\.)'")
    string = re.compile(rb"(u8|L|u|U)?\".*?\"s?")
    raw_string = re.compile(rb"(u8|L|u|U)?\"\(.*?\)\"s?")

    _basic_litarals = (
        int,
        bin_int,
        oct_int,
        hex_int,
        pointfloat,
        intfloat,
        bool,
        char,
        string,
        raw_string,
    )
    user_literal = re.compile(
        b"("
        + b"|".join(rf"({line.pattern})".encode() for line in _basic_litarals)
        + b")_"
        + name.pattern
    )  # ?

    _operators = (
        b"::",
        b".*",
        b"->*",
        b"?",
        b":",
        b"*=",
        b"/=",
        b"%=",
        b"+=",
        b"-=",
        b"<<=",
        b">>=",
        b"&=",
        b"|=",
        b"^=",
        b",",
        b"...",
        b".",
        b"->",
        b"[",
        b"]",
        b"(",
        b")",
        b"++",
        b"--",
        b"~",
        b"!=",
        b"!",
        b"-",
        b"+",
        b"*",
        b"/",
        b"%",
        b"<<",
        b">>",
        b"<=",
        b">=",
        b"<",
        b">",
        b"==",
        b"&&",
        b"||",
        b"&",
        b"^",
        b"|",
        b"=",
    )
    _delimiters = (b"{", b"}", b"\\", b":", b";", b"'", b'"')

    operator = re.compile(b"(" + b"|".join(re.escape(op) for op in _operators) + b")")
    delimiter = re.compile(b"(" + b"|".join(re.escape(op) for op in _delimiters) + b")")

    ignore = re.compile(rb"\s+")

    rules = (
        preprocessor_directive,
        comment,
        name,
        pointfloat,
        intfloat,
        bin_int,
        hex_int,
        oct_int,
        int,
        bool,
        char,
        string,
        raw_string,
        user_literal,
        operator,
        delimiter,
        ignore,
    )

    func_macro_def = re.compile(rb"#define +([a-zA-Z_][a-zA-Z0-9_]*)\(.*\) +.*$")

    def tokenize(self, source: bytes) -> list[bytes]:
        res = []

        func_macros = [b"assert"]

        now = 0
        macro_par_level = -1
        while now < len(source):
            for rule in self.rules:
                m = rule.match(source, now)
                if not m:
                    continue

                fmm = self.func_macro_def.match(m.group(0))
                if fmm:
                    func_macros.append(fmm.group(1))
                    res.append(m.group(0))

                elif macro_par_level != -1:
                    if m.group(0) == b"(":
                        macro_par_level += 1
                    elif m.group(0) == b")":
                        macro_par_level -= 1

                    res[-1] += m.group(0)

                    if macro_par_level == 0:
                        macro_par_level = -1

                elif rule == self.name and m.group(0) in func_macros:
                    macro_par_level = 0
                    res.append(m.group(0))

                elif rule != self.ignore:
                    res.append(m.group(0))

                else:
                    assert rule == self.ignore

                now = m.end()
                break

            else:
                raise Exception(f"tokenize failed at {now}, {res}")

        return res

    def tokenize_1k(self, source: bytes) -> list[bytes]:
        res = self.tokenize(source)

        while len(res) > 1000:
            while True:
                i = secrets.randbelow(len(res) - 1)
                if not res[i + 1].startswith(b"#"):
                    break

            res[i] += b"\n" + res.pop(i + 1)

        return res
