from tokens import *

DEBUG_MODE = False

def text_red(msg: str) -> str:
    return f"\033[91m{msg}\033[0m"

def text_yellow(msg: str) -> str:
    return f"\u001b[33m{msg}\033[0m"

def text_blue(msg: str) -> str:
    return f"\033[94m{msg}\033[0m"

def text_green(msg: str) -> str:
    return f"\033[92m{msg}\033[0m"


def err(msg: str):
    print(f"{text_red('error')}: {msg}")
    exit(1)

def warn(msg: str):
    print(f"{text_yellow('warning')}: {msg}")

def interupt(msg: str):
    print(f"{text_green('interupt')}: {msg}")
    exit()

def debug(msg: str, tokens: list[Token] = None):
    if not DEBUG_MODE:
        return
    print(f"{text_blue('debug')}: {msg}", end="")
    if tokens:
        s = ""
        for t in tokens:
            s += t.lexeme
        print(f", tokens: {s}", end="")
    print()


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


def inspect_stmt(stmt: Statement, indent: int = 0):
    tab = "\t" * indent
    print(f"""{tab}{stmt.type}\
{'' if not stmt.name else f': {stmt.name.lexeme}'}\
{'' if not stmt.vtype else f' ({stmt.vtype.str()})'}\
    """)
    if stmt.block:
        for s in stmt.block.stmts:
            inspect_stmt(s, indent+1)