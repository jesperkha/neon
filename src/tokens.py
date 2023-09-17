from hashlib import sha256

class Token:
    def __init__(self,
            typ: int,             # Token type
            lexeme: str,          # Token text lexeme
            line: int,            # Line number
            col: int,             # Column
            string: str,          # Line token is at as a string
            kind: str,            # Token type kind
            isfloat: bool = False # If token is float
        ):
        self.type    = typ
        self.lexeme  = lexeme
        self.line    = line
        self.col     = col
        self.string  = string
        self.kind    = kind
        self.isfloat = isfloat


class Signature:
    def __init__(self, some: object = None):
        self.sign = ""
        if some:
            self.add(some)
    
    def add(self, some: object):
        if hasattr(some, "signature"):
            self.add(some.signature)
        elif type(some) == list:
            for n in some:
                self.add(n)
        elif type(some) == Signature:
            self.sign += f"{some.sign}"
        elif type(some) == str:
            self.sign += f".{some}"
        else:
            self.sign += f".{type(some).__name__}"
    
    # Returns the sha256 hexadecimal value of the signature
    def hash(self) -> str:
        return sha256(self.sign.encode("utf-8")).hexdigest()
    
    # Returns the short representation of the signature
    def short(self) -> str:
        s = self.sign.split(".")
        t = [c[0].upper() if len(c) != 0 else "" for c in s]
        return "".join(t)
    
    def __str__(self) -> str:
        return self.sign

    def __eq__(self, __value: object) -> bool:
        return self.sign == __value.sign
    

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

# Keywords
RETURN        = i()
FUNC          = i()
IF            = i()
ELSE          = i()
ELIF          = i()

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
TYPE_NONE   = "none_t"
TYPE_NULL   = "null_t"
TYPE_ANY    = "any_t"
TYPE_STRING = "string_t"
TYPE_CHAR   = "char_t"
TYPE_BYTE   = "byte_t"
TYPE_FLOAT  = "float_t"
TYPE_I8     = "i8_t"
TYPE_I16    = "i16_t"
TYPE_I32    = "i32_t"
TYPE_I64    = "i64_t"
TYPE_U8     = "u8_T"
TYPE_U16    = "u16_t"
TYPE_U32    = "u32_t"
TYPE_U64    = "u64_t"
TYPE_F32    = "f32_t"
TYPE_F64    = "f64_t"
TYPE_BOOL   = "bool_t"
TYPE_FUNC   = "function_t"
TYPE_ARRAY  = "array_t"
TYPE_STRUCT = "struct_t"

# Type kinds. Used to compare expression values in static analysis
NUMBER_KINDS = (
    TYPE_I8,
    TYPE_I16,
    TYPE_I32,
    TYPE_I64,
    TYPE_U8,
    TYPE_U16,
    TYPE_U32,
    TYPE_U64,
    TYPE_F32,
    TYPE_F64,
    TYPE_BYTE
)

KIND_NONE   = "K_NONE"
KIND_STRING = "K_STRING"
KIND_NUMBER = "K_NUMBER"
KIND_BOOL   = "K_BOOL"
KIND_ARRAY  = "K_ARRAY"
KIND_STRUCT = "K_STRUCT"

kind_to_types = {
    KIND_NUMBER: NUMBER_KINDS,
    KIND_STRING: [TYPE_STRING, TYPE_CHAR],
    KIND_BOOL: [TYPE_BOOL],
    KIND_ARRAY: [TYPE_ARRAY],
    KIND_STRUCT: [TYPE_STRUCT],
    KIND_NONE: [TYPE_NONE, TYPE_NULL],
}

type_to_kind = {}
for k, v in kind_to_types.items():
    for t in v: type_to_kind[t] = k

keyword_lookup = {
    "return": RETURN,
    "func":   FUNC,
    "true":   TRUE,
    "false":  FALSE,
    "in":     IN,
    "if":     IF,
    "else":   ELSE,
    "elif":   ELIF,
    "null":   NULL,
}

typeword_lookup = {
    "none":   TYPE_NONE,
    "int":    TYPE_I32,
    "float":  TYPE_F32,
    "bool":   TYPE_BOOL,
    "string": TYPE_STRING,
    "char":   TYPE_CHAR,
    "byte":   TYPE_BYTE,
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

double_symbol_lookup = {
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

binary_ops = (
    AND,
    OR,
    EQUAL_EQUAL,
    NOT_EQUAL,
    GREATER_EQUAL,
    LESS_EQUAL,
    GREATER,
    LESS,
    PLUS,
    MINUS,
    STAR,
    SLASH,
    MODULO,
)

unary_ops = (
    MINUS,
    NOT,
)

whitespace_lookup = {
    " ": SPACE,
    "\n": NEWLINE,
    "\t": TAB
}

__lookup = keyword_lookup.copy()
__lookup.update(typeword_lookup.copy())
__lookup.update(symbol_lookup.copy())
__lookup.update(double_symbol_lookup.copy())
all_tokens = {v: k for k, v in __lookup.items()}