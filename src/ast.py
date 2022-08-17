from tokens import *
import util

class AstNode:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.stmts = []
        self.indent = 0

    def print(self):
        for node in self.stmts:
            self.indent = -1
            s = self.string_node(node)
            print(s)

    def concat(self, title: str, suffix: str, end: str = "\n") -> str:
        return f"{self.indent*'  '}{title}: {end}{suffix}"

    def indent_wrap(func):
        def wrap(self, node):
            self.indent += 1
            s = func(self, node)
            self.indent -= 1
            return s

        return wrap

    @indent_wrap
    def string_node(self, node) -> str:
        t = type(node)
        if t == ExprStmt:
            return self.concat("ExprStmt", self.string_node(node.expr))
        
        elif t == Literal:
            return self.concat("Literal", node.token.lexeme, "")

        elif t == Variable:
            return self.concat("Variable", node.token.lexeme, "")
        
        elif t == Group:
            return self.concat("Group", self.string_node(node.inner))

        elif t == Binary:
            self.indent += 1
            left = self.concat(".left", self.string_node(node.left))
            right = self.concat(".right", self.string_node(node.right))
            op = self.concat(".op", node.op.lexeme, "")
            self.indent -= 1
            return self.concat("Binary", f"{left}\n{right}\n{op}")

        return ""

class Stmt(AstNode):
    def __init__(self):
        self.tokens = []

class Expr(AstNode):
    def __init__(self):
        self.tokens = []

# ------------ STATEMENTS ------------ 

class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

# ----------- EXPRESSIONS ------------

class Literal(Expr):
    def __init__(self, tok: Token):
        super().__init__()
        self.token = tok

class Variable(Expr):
    def __init__(self, tok: Token):
        super().__init__()
        self.token = tok

class Group(Expr):
    def __init__(self, inner: Expr):
        super().__init__()
        self.tokens = []
        self.inner = inner

class Binary(Expr):
    def __init__(self, left: Expr, right: Expr, op: Token):
        super().__init__()
        self.left = left
        self.right = right
        self.op = op
