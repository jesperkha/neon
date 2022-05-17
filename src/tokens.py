class Token:
    def __init__(self, type: int, lexeme: str, line: int):
        self.lexeme  = lexeme
        self.line    = line
        self.type    = type
        self.isfloat = False

class Type:
    def __init__(self):
        pass

class Expression:
    def __init__(self, type: str, tokens: list, line: int):
        self.type = type
        self.line = line
        self.tokens = tokens
        self.exprs:    list[Expression] = None
        self.left:     Expression = None
        self.right:    Expression = None
        self.inner:    Expression = None
        self.array:    Expression = None
        self.callee:   Token = None
        self.operator: Token = None

class Statement:
    def __init__(self, type: str, line: int):
        self.type  = type
        self.line  = line
        self.expr: Expression = None
        self.block: Statement = None
        self.name: Token = None
        self.vtype: Type = None
        self.stmts: list = []

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
RETURN        = i()
FUNC          = i()
COLON         = i()

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
STMT_NONE   = "UNCOMPLETE_STMT"
STMT_EXPR   = "EXPR"
STMT_RETURN = "RETURN"
STMT_FUNC   = "FUNCTION"
STMT_BLOCK  = "BLOCK"

keyword_lookup = {
    "return": RETURN,
    "func":   FUNC,
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
    ":": COLON,
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