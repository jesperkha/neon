from tokens import *

def err(msg: str) -> None:
    print(msg)
    exit(1)


def seek(tokens: list[Token], start_t: int, end_t: int) -> int:
    "Seeks and returns the index of the closing token of a given list."
    if tokens[0].type != start_t:
        return -1

    t = 0
    for idx, tok in enumerate(tokens):
        if tok.type == start_t:
            t += 1
        elif tok.type == end_t:
            t -= 1
        if t == 0:
            return idx

    return -1


def inspect_expr(expr: Expression, prefix: str = "", level: int = -1):
    "Pints out formatted expression"
    s = ""
    for t in expr.tokens: s += t.lexeme
    tabs = "\t" * level
    print(f"{tabs}{prefix + ': ' if prefix != '' else ''}{expr.type} '{s}'")
    if expr.operator:
        tabs2 = "\t" * (level + 1)
        print(f"{tabs2}operator: '{expr.operator.lexeme}'")
    a = (expr.inner, expr.left, expr.right)
    b = ("inner", "left", "right")
    for idx, v in enumerate(a):
        if v: inspect_expr(v, b[idx], level+1)


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