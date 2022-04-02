LBRACE = "lbrace"
RBRACE = "rbrace"
LBRACKET = "lbracket"
RBRACKET = "rbracket"
STR = "str"
NUMBER = "number"
COLON = "colon"
COMMA = "comma"


JSON_TOKEN_REGEXPS = {
    LBRACE: r"{",
    RBRACE: r"}",
    LBRACKET: "\\[",
    RBRACKET: "\\]",
    STR: r'"[^"]*"',
    NUMBER: r'([0-9]*[.])?[0-9]+',
    COLON: r":",
    COMMA: r",",
}