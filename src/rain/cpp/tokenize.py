import re
import secrets


class Tokenizer:
    preprocessor_directive = re.compile(r"^#.*$", re.MULTILINE)
    comment = re.compile(r"(//[^\n]*?$)|(/\*.*?\*/)", re.DOTALL | re.MULTILINE)

    name = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")  # keyword, identifier

    pointfloat = re.compile(r"\d('?\d)*\.(\d('?\d)*)?([eE]-?\d('?\d)*)?[fFlL]?")
    intfloat = re.compile(r"\d('?\d)*[eE]-?\d('?\d)*[fFlL]?")

    bin_int = re.compile(r"0[bB][01]('?[01])*[uU]?[lL]{0,2}")
    hex_int = re.compile(r"0[xX][0-9a-fA-F]('?[0-9a-fA-F])*[uU]?[lL]{0,2}")
    oct_int = re.compile(r"0('?[0-7])*[uU]?[lL]{0,2}")
    int = re.compile(r"\d('?\d)*[uU]?[lL]{0,2}")

    bool = re.compile(r"(true|false)")

    char = re.compile(r"(u8|L|u|U)?'(.|\\.)'")
    string = re.compile(r"(u8|L|u|U)?\".*?\"s?")
    raw_string = re.compile(r"(u8|L|u|U)?\"\(.*?\)\"s?")

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
        "(" + "|".join(rf"({l.pattern})" for l in _basic_litarals) + ")_" + name.pattern
    )  # ?

    _operators = (
        "::",
        ".*",
        "->*",
        "?",
        ":",
        "*=",
        "/=",
        "%=",
        "+=",
        "-=",
        "<<=",
        ">>=",
        "&=",
        "|=",
        "^=",
        ",",
        "...",
        ".",
        "->",
        "[",
        "]",
        "(",
        ")",
        "++",
        "--",
        "~",
        "!=",
        "!",
        "-",
        "+",
        "*",
        "/",
        "%",
        "<<",
        ">>",
        "<=",
        ">=",
        "<",
        ">",
        "==",
        "&&",
        "||",
        "&",
        "^",
        "|",
        "=",
    )
    _delimiters = ("{", "}", "\\", ":", ";", "'", '"')

    operator = re.compile("(" + "|".join(re.escape(op) for op in _operators) + ")")
    delimiter = re.compile("(" + "|".join(re.escape(op) for op in _delimiters) + ")")

    ignore = re.compile(r"\s+")

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

    func_macro_def = re.compile(r"#define +([a-zA-Z_][a-zA-Z0-9_]*)\(.*\) +.*$")

    def tokenize(self, source: str) -> list[str]:
        res = []

        func_macros = ["assert"]

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
                    if m.group(0) == "(":
                        macro_par_level += 1
                    elif m.group(0) == ")":
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

    def tokenize_1k(self, source: str) -> list[str]:
        res = self.tokenize(source)

        while len(res) > 1000:
            while True:
                i = secrets.randbelow(len(res) - 1)
                if not res[i + 1].startswith("#"):
                    break

            res[i] += "\n" + res.pop(i + 1)

        return res
