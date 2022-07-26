class Token:
    def __init__(self, typ: int, lexeme: str, line: int, col: int, isfloat: int = False):
        self.type    = typ
        self.lexeme  = lexeme
        self.line    = line
        self.column  = col
        self.isfloat = isfloat

class Node:
    def __init__(self):
        pass
    
class Separator:
    def __init__(self, *args):
        self.args = args

class Type:
    def __init__(self, typ: str, name: str = ""):
        self.type = typ
        self.subtype = Type(TYPE_NONE)

        # Set printable name
        if typ not in (TYPE_ARRAY, TYPE_STRUCT):
            self.name = typ.lower()
        elif typ == TYPE_ARRAY:
            self.name = "[]"
        elif typ == TYPE_STRUCT:
            self.name = name

        # Set type kind
        for key, val in type_to_kind.items():
            if self.type in val:
                self.kind = key


_i = 0
def i():
    global _i
    _i += 1
    return _i

# Token types
NULL          = i()
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

# Binary operators in order of precedency
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

# Unary operators in order of precedency
BIT_RSHIFT    = i()
BIT_NEGATE    = i()
NOT           = i()
REFERENCE     = i()

# Expression types
EXPR          = "EXPRESSION"
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
STMT_EXPR    = "EXPR"
STMT_RETURN  = "RETURN"
STMT_FUNC    = "FUNCTION"
STMT_BLOCK   = "BLOCK"
STMT_DECLARE = "DECLARATION"
STMT_ASSIGN  = "ASSIGNMENT"
STMT_PRINT   = "PRINT"

# Types
TYPE_NONE   = "NONE"
TYPE_NULL   = "NULL"
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
TYPE_FUNC   = "FUNCTION"
TYPE_ARRAY  = "ARRAY"
TYPE_STRUCT = "STRUCT"

# Type kinds
KIND_NONE   = "K_NONE"
KIND_STRING = "K_STRING"
KIND_NUMBER = "K_NUMBER"
KIND_BOOL   = "K_BOOL"
KIND_ARRAY  = "K_ARRAY"
KIND_STRUCT = "K_STRUCT"

NUMBER_KINDS = (
    TYPE_INT,
    TYPE_I8,
    TYPE_I16,
    TYPE_I32,
    TYPE_I64,
    TYPE_U8,
    TYPE_U16,
    TYPE_U32,
    TYPE_U64,
    TYPE_FLOAT,
    TYPE_F32,
    TYPE_F64
)

STRING_KINDS = (
    TYPE_STRING,
    TYPE_CHAR
)

BOOL_KINDS = (
    TYPE_BOOL
)

ARRAY_KINDS = (
    TYPE_ARRAY
)

STRUCT_KINDS = (
    TYPE_STRUCT
)

NONE_KINDS = (
    TYPE_NONE,
    TYPE_NULL
)

type_to_kind = {
    KIND_NUMBER: NUMBER_KINDS,
    KIND_STRING: STRUCT_KINDS,
    KIND_BOOL: BOOL_KINDS,
    KIND_ARRAY: ARRAY_KINDS,
    KIND_STRUCT: STRUCT_KINDS,
    KIND_NONE: NONE_KINDS
}

keyword_lookup = {
    "return": RETURN,
    "func":   FUNC,
    "true":   TRUE,
    "false":  FALSE,
    "in":     IN,
    "null":   NULL
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
    # "&": BIT_AND,
    # "|": BIT_OR,
    # "~": BIT_NEGATE,
    # "^": BIT_XOR,
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
    # ">>": BIT_RSHIFT,
    # "<<": BIT_LSHIFT,
}

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}
