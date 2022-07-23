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
    
    def __str__(self) -> str:
        return self.lexeme

class Type:
    def __init__(self, typ: str, compl: str = "", sub_type = None, negative: bool = False, empty: bool = False):
        self.type = typ
        self.set_kind()

        self.negative = negative
        self.float = self.type in (TYPE_F32, TYPE_FLOAT, TYPE_F64)

        # Complex type name formed after init
        self.complex = compl
        self.sub_type = sub_type
        
        # For comparing arrays
        self.empty = empty
    
    def set_kind(self):
        if self.type in (TYPE_BOOL):
            self.kind = KIND_BOOL
        elif self.type in (TYPE_INT, TYPE_I8, TYPE_I16, TYPE_I32, TYPE_I64, TYPE_U8, TYPE_U16, TYPE_U32, TYPE_U64, TYPE_FLOAT, TYPE_F32, TYPE_F64):
            self.kind = KIND_NUMBER
        elif self.type in (TYPE_CHAR, TYPE_STRING):
            self.kind = KIND_STRING
        elif self.type == TYPE_ARRAY:
            self.kind = KIND_ARRAY
        else:
            self.kind = KIND_NONE

    def append_type(self, t):
        if self.type == TYPE_NONE:
            self.type = t.type
            self.set_kind()
        elif self.sub_type:
            self.sub_type.append_type(t)
        else:
            self.sub_type = t
    
    def str(self) -> str:
        if self.sub_type:
            return self.complex + self.sub_type.str()

        return self.type

    def compare_arrays(self, a, b) -> bool:
        if a.sub_type == b.sub_type:
            return True

        if a.empty or b.empty:
            return True

        if (not a.sub_type and b.sub_type) or (a.sub_type and not b.sub_type):
            return True

        if a.sub_type == b.sub_type == TYPE_ARRAY:
            return self.compare_arrays(a.sub_type, b.sub_type)

        return a.str() == b.str()

    def __eq__(self, o: object) -> bool:
        if type(o) == str: # allow checking for type constant
            return self.type == o

        if TYPE_ANY in (self.type, o.type):
            return True

        if self.type == TYPE_ARRAY and o.type == TYPE_ARRAY:
            return self.compare_arrays(self, o)

        return self.str() == o.str()
    
    def __bool__(self) -> bool:
        return self.type != TYPE_NONE

    def __str__(self) -> str:
        return self.str().lower()

class Expression:
    def __init__(self, typ: str, tokens: list, line: int):
        self.type = typ
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
    def __init__(self, typ: str, line: int):
        self.type  = typ
        self.line  = line
        self.expr: Expression = None
        self.block: Statement = None
        self.name: Token = None
        self.vtype: Type = Type(TYPE_NONE)
        self.stmts: list = []
        # list of tuple(name, Type)
        self.params: list = []

class ScannedStmt:
    def __init__(self, stmt: Statement):
        self.stmt = stmt

_i = 0
def i():
    global _i
    _i += 1
    return _i

# Token types
IDENTIFIER    = i()
TRUE          = i()
FALSE         = i()
NUMBER        = i()
STRING        = i()
CHAR          = i()

NEWLINE       = i()
SPACE         = i()
TAB           = i()
COMMENT       = i()

EQUAL         = i()
COLON_EQUAL   = i()
COLON         = i()
COMMA         = i()

LEFT_PAREN    = i()
RIGHT_PAREN   = i()
LEFT_BRACE    = i()
RIGHT_BRACE   = i()
LEFT_SQUARE   = i()
RIGHT_SQUARE  = i()

RETURN        = i()
FUNC          = i()

# Binary expression tokens in order of precedency
AND           = i()
OR            = i()
EQUAL_EQUAL   = i()
NOT_EQUAL     = i()
IN            = i()
GREATER       = i()
LESS          = i()
GREATER_EQUAL = i()
LESS_EQUAL    = i()
PLUS          = i()
MINUS         = i()
STAR          = i()
SLASH         = i()
MODULO        = i()
BIT_OR        = i()
BIT_XOR       = i()
BIT_AND       = i()
BIT_LSHIFT    = i()
BIT_RSHIFT    = i()
BIT_NEGATE    = i()
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
KIND_NUMBER = "K_NUMBER"
KIND_BOOL   = "K_BOOL"
KIND_ARRAY  = "K_ARRAY"

# Types
TYPE_NONE   = "NONE"
TYPE_ANY    = "ANY"
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
TYPE_FUNC   = "FUNCTION"
TYPE_ARRAY  = "ARRAY"

# TYPE_INT is also in this collection to include number literals (negatives checked at runtime)
COLLECTION_UNSIGNED = (TYPE_INT, TYPE_U8, TYPE_U16, TYPE_U32, TYPE_U64)

keyword_lookup = {
    "return": RETURN,
    "func":   FUNC,
    "true":   TRUE,
    "false":  FALSE,
    "in":     IN,
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
    "&": BIT_AND,
    "|": BIT_OR,
    "~": BIT_NEGATE,
    "^": BIT_XOR,
}

double_token_lookup = {
    "==": EQUAL_EQUAL,
    ">=": GREATER_EQUAL,
    "<=": LESS_EQUAL,
    "!=": NOT_EQUAL,
    "&&": AND,
    "||": OR,
    ":=": COLON_EQUAL,
    "//": COMMENT,
    ">>": BIT_RSHIFT,
    "<<": BIT_LSHIFT,
}

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}

binary_op_combos = {
        KIND_NUMBER: (PLUS, MINUS, STAR, SLASH, MODULO, NOT_EQUAL, EQUAL_EQUAL, GREATER, LESS, GREATER_EQUAL, LESS_EQUAL),
    KIND_STRING: (PLUS, NOT_EQUAL, EQUAL_EQUAL),
    KIND_ARRAY: (PLUS, NOT_EQUAL, EQUAL_EQUAL),
    KIND_BOOL: (AND, OR, EQUAL_EQUAL, NOT_EQUAL),
}
