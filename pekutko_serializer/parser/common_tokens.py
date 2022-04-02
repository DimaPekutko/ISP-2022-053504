LBRACE = "lbrace"
RBRACE = "rbrace"
LBRACKET = "lbracket"
RBRACKET = "rbracket"
STR = "str"
NUMBER = "number"
BOOL = "bool"
COLON = "colon"
COMMA = "comma"


TOKEN_REGEXPS = {
    LBRACE: r"{",
    RBRACE: r"}",
    LBRACKET: "\\[",
    RBRACKET: "\\]",
    STR: r'"[^"]*"',
    NUMBER: r'([0-9]*[.])?[0-9]+',
    BOOL: r'^(?:tru|fals)e',
    COLON: r":",
    COMMA: r",",
}