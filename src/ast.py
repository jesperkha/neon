from tokens import *

class AstNode:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

class Stmt(AstNode):
    pass

class Expr(AstNode):
    pass

class Literal(Expr):
    pass
