from tokens import *

DEBUG_MODE = False

def err(msg: str) -> None:
    print(f"error: {msg}")
    exit(1)


def debug(msg: str, tokens: list[Token] = None) -> None:
    if not DEBUG_MODE:
        return
        
    print(f"debug: {msg}", end="")
    if tokens:
        s = ""
        for t in tokens:
            s += t.lexeme
        print(f", tokens: {s}", end="")
    print()


def inspect_expr(expr: Expression, prefix: str = "", level: int = -1):
    "Pints out formatted expression"
    s = ""
    for t in expr.tokens: s += t.lexeme
    tabs = "\t" * level
    print(f"{tabs}{prefix + ': ' if prefix != '' else ''}{expr.type} '{s}'")

    a = (expr.operator, expr.callee)
    b = ("operator", "callee")
    tabs2 = "\t" * (level + 1)
    for idx, v in enumerate(a):
        if v: print(f"{tabs2}{b[idx]}: '{v.lexeme}'")

    a = (expr.inner, expr.left, expr.right)
    b = ("inner", "left", "right")
    for idx, v in enumerate(a):
        if v: inspect_expr(v, b[idx], level+1)
    
    if expr.exprs:
        for i, e in enumerate(expr.exprs):
            inspect_expr(e, f"{i}", level+1)


def inspect_types(expr: Expression):
    "Prints expression with values substituted with their types"
    s = ""
    typ = Type()
    for t in expr.tokens:
        vtype = typ.setv(t)
        if vtype != TYPE_NONE:
            s += vtype
        else:
            s += t.lexeme
    
    print(s)


def inspect_stmt(stmt: Statement):
    pass