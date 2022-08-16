from tokens import *

class AstNode:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

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
