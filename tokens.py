class Token:
    def __init__(self, type: int, lexeme: str, line: int) -> None:
        self.lexeme = lexeme
        self.line   = line
        self.type   = type
        self.isfloat = False

class Expression:
    def __init__(self, type: str, tokens: list, line: int) -> None:
        self.type = type
        self.tokens = tokens
        self.line = line
        self.left = None
        self.right = None
        self.value = None
        self.operator = None

class Statement:
    def __init__(self, type: str, expr: Expression, line: int) -> None:
        self.type = type
        self.line = line
        self.expr = expr

_i = 0
def i():
    global _i
    _i += 1
    return _i

# Token types
EQUAL        = i()
IDENTIFIER   = i()
NUMBER       = i()
SPACE        = i()
NEWLINE      = i()
TAB          = i()
EQUAL_EQUAL  = i()
STRING       = i()
LEFT_PAREN   = i()
RIGHT_PAREN  = i()
LEFT_BRACE   = i()
RIGHT_BRACE  = i()
PLUS         = i()
MINUS        = i()
STAR         = i()
SLASH        = i()
LEFT_SQUARE  = i()
RIGHT_SQUARE = i()

# Expression types
EMPTY_EXPR   = "EMPTY_EXPR"
BINARY_EXPR  = "BINARY_EXPR"
GROUP_EXPR   = "GROUP_EXPR"
LITERAL_EXPR = "LITERAL_EXPR"
ARRAY_EXPR   = "ARRAY_EXPR"

# Statement types
EXPR_STMT = "EXPR_STMT"

keyword_lookup = {
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
    "[": LEFT_SQUARE,
    "]": RIGHT_SQUARE,
}

double_token_lookup = {
    "==": EQUAL_EQUAL,
}

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}