from tokens import *

class AstNode:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.stmts = []

class Stmt(AstNode):
    pass

class Expr(AstNode):
    pass

# ------------ STATEMENTS ------------ 

class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

# ----------- EXPRESSIONS ------------

class Literal(Expr):
    def __init__(self, tok: Token):
        self.token = tok

class Variable(Expr):
    def __init__(self, tok: Token):
        self.token = tok

class Group(Expr):
    def __init__(self, inner: Expr):
        self.inner = inner
