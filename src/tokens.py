class Token:
    def __init__(self, type: int, lexeme: str, line: int) -> None:
        self.lexeme  = lexeme
        self.line    = line
        self.type    = type
        self.isfloat = False

class Type:
    def __init__(self, type: str = "") -> None:
        self.type  = type
        self.group: str
        self.set(type)

    def set(self, type: str) -> None:
        "set group from value type"
        self.type = type
        if type in (TYPE_CHAR, TYPE_STRING):
            self.group = GRP_STRING
        elif type in (TYPE_INT):
            self.group = GRP_NUMBER
        else:
            self.group = GRP_NONE
    
    def setv(self, token: Token) -> str:
        "set value type and group from token type, returns vtype"
        t = token.type
        if t == STRING:
            self.set(TYPE_STRING)
        elif t == NUMBER:
            self.set(TYPE_FLOAT if token.isfloat else TYPE_INT)
        elif t == IDENTIFIER:
            self.set(TYPE_VAR)
        else:
            self.set(TYPE_NONE)
        return self.type
    
class Expression:
    def __init__(self, type: str, tokens: list, line: int) -> None:
        self.type = type
        self.tokens = tokens
        self.line = line
        self.left: Expression = None
        self.right: Expression = None
        self.inner: Expression = None
        self.operator: Token = None
        self.callee: Token = None
        self.array: Expression = None
        self.exprs: list[Expression] = None
        self.value = Type()
        if self.type == EXPR_LITERAL:
            self.value.setv(self.tokens[0])

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
EQUAL         = i()
IDENTIFIER    = i()
NUMBER        = i()
SPACE         = i()
NEWLINE       = i()
TAB           = i()
STRING        = i()
LEFT_PAREN    = i()
RIGHT_PAREN   = i()
LEFT_BRACE    = i()
RIGHT_BRACE   = i()
LEFT_SQUARE   = i()
RIGHT_SQUARE  = i()
COMMA         = i()

# Binary expression tokens in order of precedency
AND           = i()
OR            = i()
GREATER       = i()
LESS          = i()
EQUAL_EQUAL   = i()
NOT_EQUAL     = i()
GREATER_EQUAL = i()
LESS_EQUAL    = i()
PLUS          = i()
MINUS         = i()
STAR          = i()
SLASH         = i()
MODULO        = i()
NOT           = i()

# Expression types
EXPR_EMPTY    = "EMPTY"
EXPR_BINARY   = "BINARY"
EXPR_GROUP    = "GROUP"
EXPR_LITERAL  = "LITERAL"
EXPR_ARRAY    = "ARRAY"
EXPR_UNARY    = "UNARY"
EXPR_CALL     = "CALL"
EXPR_INDEX    = "INDEX"
EXPR_VARIABLE = "VARIABLE"
EXPR_ARGS     = "ARGS"

# Statement types
STMT_EXPR = "EXPR"

# Types
TYPE_NONE   = "NONE"
TYPE_STRING = "STRING"
TYPE_CHAR   = "CHAR"
TYPE_INT    = "INT"
TYPE_FLOAT  = "FLOAT"
TYPE_VAR    = "UNKNOWN"

# Type groups
GRP_NONE   = "NONE"
GRP_STRING = "STRING"
GRP_NUMBER = "NUMBER"

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
    "!": NOT,
    "%": MODULO,
    ">": GREATER,
    "<": LESS,
    ",": COMMA,
}

double_token_lookup = {
    "==": EQUAL_EQUAL,
    ">=": GREATER_EQUAL,
    "<=": LESS_EQUAL,
    "!=": NOT_EQUAL,
    "&&": AND,
    "||": OR,
}

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}