# Token definitions and data types
# 
# This file contains definitions for neons keywords, symbols, and data structures like ASTs.
# Almost all other parts of the compiler uses this file. The definitions are made as dynamic
# as possible to make it easy to add or remove tokens, type, or keywords.

class Token:
    def __init__(self, type: int, lexeme: str, line: int):
        self.lexeme  = lexeme
        self.line    = line
        self.type    = type
        self.isfloat = False

class Type:
    def __init__(self, type: str, complex: list = None):
        self.type = type
        self.set_kind()
        # list of types in order of definition
        self.complex: list[str] = complex
        if not self.complex:
            self.complex = [self.type]
    
    def set_kind(self):
        if self.type in (TYPE_BOOL):
            self.kind = KIND_BOOL
        elif self.type in (TYPE_INT, TYPE_I8, TYPE_I16, TYPE_I32, TYPE_I64):
            self.kind = KIND_INT
        elif self.type in (TYPE_FLOAT, TYPE_F32, TYPE_F64):
            self.kind = KIND_FLOAT
        elif self.type in (TYPE_CHAR, TYPE_STRING):
            self.kind = KIND_STRING
        else:
            self.kind = KIND_NONE
    
    def str(self) -> str:
        return "".join(self.complex)

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
COLON_EQUAL   = i()
PRINT         = i()

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
STMT_NONE    = "UNCOMPLETE_STMT"
STMT_EXPR    = "EXPR"
STMT_RETURN  = "RETURN"
STMT_FUNC    = "FUNCTION"
STMT_BLOCK   = "BLOCK"
STMT_DECLARE = "DECLARATION"
STMT_ASSIGN  = "ASSIGNMENT"
STMT_PRINT   = "PRINT"

# Type kinds
KIND_NONE   = "K_NONE"
KIND_STRING = "K_STRING"
KIND_INT    = "K_INT"
KIND_FLOAT  = "K_FLOAT"
KIND_BOOL   = "K_BOOL"

# Types
TYPE_NONE   = "NONE"
TYPE_STRING = "STRING"
TYPE_CHAR   = "CHAR"
TYPE_INT    = "INT"
TYPE_FLOAT  = "FLOAT"
TYPE_I8     = "I8"
TYPE_I16    = "I16"
TYPE_I32    = "I32"
TYPE_I64    = "I64"
TYPE_U8     = "U8"
TYPE_U16    = "U16"
TYPE_U32    = "U32"
TYPE_U64    = "U64"
TYPE_F32    = "F32"
TYPE_F64    = "F64"
TYPE_BOOL   = "BOOL"
TYPE_USRDEF = "USER_DEFINED"

keyword_lookup = {
    "return": RETURN,
    "func":   FUNC,
    "print":  PRINT,
}

typeword_lookup = {
    "int":    TYPE_INT,
    "float":  TYPE_FLOAT,
    "bool":   TYPE_BOOL,
    "string": TYPE_STRING,
    "char":   TYPE_CHAR,
    "i8":     TYPE_I8,
    "i16":    TYPE_I16,
    "i32":    TYPE_I32,
    "i64":    TYPE_I64,
    "u8":     TYPE_U8,
    "u16":    TYPE_U16,
    "u32":    TYPE_U32,
    "u64":    TYPE_U64,
    "f32":    TYPE_F32,
    "f64":    TYPE_F64,
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
    ":=": COLON_EQUAL,
}

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}