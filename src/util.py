from tokens import *

DEBUG_MODE = False

def err(msg: str):
    print(f"\033[91merror\033[0m: {msg}")
    exit(1)


def debug(msg: str, tokens: list[Token] = None):
    if not DEBUG_MODE:
        return
    print(f"\033[94mdebug:\033[0m {msg}", end="")
    if tokens:
        s = ""
        for t in tokens:
            s += t.lexeme
        print(f", tokens: {s}", end="")
    print()


def interupt(msg: str):
    print(f"\033[92minterupt:\033[0m {msg}")
    exit()


def inspect_expr(expr: Expression, prefix: str = "", level: int = -1):
    "Pints out formatted expression"
    tabs = "\t" * level
    if expr.type == EXPR_EMPTY:
        print(f"{tabs}EMPTY_EXPR")
        return
        
    s = ""
    for t in expr.tokens: s += t.lexeme
    print(f"{tabs}{prefix + ': ' if prefix != '' else ''}{expr.type} '{s}'")

    a = (expr.operator, expr.callee)
    b = ("operator", "callee")
    tabs2 = "\t" * (level + 1)
    for idx, v in enumerate(a):
        if v: print(f"{tabs2}{b[idx]}: '{v.lexeme}'")

    a = (expr.inner, expr.left, expr.right, expr.array)
    b = ("inner", "left", "right", "array")
    for idx, v in enumerate(a):
        if v: inspect_expr(v, b[idx], level+1)
    
    if expr.exprs:
        for i, e in enumerate(expr.exprs):
            inspect_expr(e, f"{i}", level+1)


def inspect_stmt(stmt: Statement):
    pass