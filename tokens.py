_i = 0
def i():
    global _i
    _i += 1
    return _i

# Token types
INT         = i()
EQUAL       = i()
IDENTIFIER  = i()
NUMBER      = i()
SPACE       = i()
NEWLINE     = i()
TAB         = i()
EQUAL_EQUAL = i()
STRING      = i()
LEFT_PAREN  = i()
RIGHT_PAREN = i()
LEFT_BRACE  = i()
RIGHT_BRACE = i()
PLUS        = i()
MINUS       = i()
STAR        = i()
SLASH       = i()

keyword_lookup = {
    "int": INT
}

symbol_lookup = {
    "+": PLUS,
    "-": MINUS,
    "*": STAR,
    "/": SLASH,
    "=": EQUAL,
    "(": LEFT_PAREN,
    ")": RIGHT_PAREN,
    "{": LEFT_BRACE,
    "}": RIGHT_BRACE,
}

double_token_lookup = {
    "==": EQUAL_EQUAL,
}

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}