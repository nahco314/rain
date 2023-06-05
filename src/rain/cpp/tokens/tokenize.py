import re


class Tokenizer:
    preprocessor_directive = re.compile(r"^#.*\n", re.MULTILINE)

    name = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")  # keyword, identifier

    bin_int = re.compile(r"0[bB][01]('?[01])*[uU]?[lL]{0,2}")
    hex_int = re.compile(r"0[xX][0-9a-fA-F]('?[0-9a-fA-F])*[uU]?[lL]{0,2}")
    oct_int = re.compile(r"0('?[0-7])*[uU]?[lL]{0,2}")
    int = re.compile(r"\d('?\d)*[uU]?[lL]{0,2}")

    pointfloat = re.compile(r"\d('?\d)*\.(\d('?\d)*)?([eE]-?\d('?\d)*)?[fFlL]")
    intfloat = re.compile(r"\d('?\d)*[eE]-?\d('?\d)*[fFlL]")

    bool = re.compile(r"(true|false)")

    char = re.compile(r"(u8|L|u|U)?'.'")
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
        "?:",
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
        ".",
        "->",
        "[",
        "]",
        "(",
        ")",
        "++",
        "--",
        "~",
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
        "!=",
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
        name,
        bin_int,
        hex_int,
        oct_int,
        int,
        pointfloat,
        intfloat,
        bool,
        char,
        string,
        raw_string,
        user_literal,
        operator,
        delimiter,
        ignore,
    )

    def tokenize(self, source: str) -> list[str]:
        res = []

        now = 0
        while now < len(source):
            for rule in self.rules:
                m = rule.match(source, now)
                if m:
                    if rule != self.ignore:
                        res.append(m.group(0))

                    now = m.end()
                    break
            else:
                raise Exception(f"tokenize failed at {now}, {res}")

        return res
