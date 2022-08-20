from tokens import *
import util

class AstNode:
    def __init__(self):
        self.stmts = []
        self.indent = 0

    def print(self):
        for node in self.stmts:
            self.indent = -1
            print(self.string_node(node))

    def print_block(self, stmts):
        for node in stmts:
            print(self.string_node(node), end="")

    def concat(self, title: str, suffix: str, end: str = "\n") -> str:
        return f"{self.indent*'| '}{title}: {end}{suffix}"

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

        elif t == Block:
            print(self.concat("Block", "", ""))
            self.print_block(node.stmts)
            return ""
        
        elif t == Declaration:
            self.indent += 1
            name = self.concat(".name", node.ident.lexeme, "")
            expr = self.concat(".expr", self.string_node(node.expr))
            self.indent -= 1
            return self.concat("Declaration", f"{name}\n{expr}")

        elif t == Assignment:
            self.indent += 1
            left = self.concat(".left", self.string_node(node.left))
            expr = self.concat(".expr", self.string_node(node.expr))
            self.indent -= 1
            return self.concat("Assignment", f"{left}\n{expr}")

        elif t == Return:
            return self.concat("Return", self.string_node(node.expr))
        
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
            return self.concat("Binary", f"{op}\n{left}\n{right}")

        elif t == Empty:
            return self.concat("Empty", "", "")

        elif t == Unary:
            self.indent += 1
            op = self.concat("op", node.op.lexeme, "")
            expr = self.concat(".expr", self.string_node(node.expr))
            self.indent -= 1
            return self.concat("Unary", f"{op}\n{expr}")

        elif t == Args:
            self.indent += 1
            args = []
            for a in node.args:
                args.append(self.string_node(a))
            self.indent -= 1
            return self.concat("Args", "\n".join(args))

        elif t == Call:
            self.indent += 1
            callee = self.concat(".callee", self.string_node(node.callee))
            inner = self.concat(".inner", self.string_node(node.inner))
            self.indent -= 1
            return self.concat("Call", f"{callee}\n{inner}")

        return ""

class Stmt(AstNode):
    pass

class Expr(AstNode):
    pass

# ------------ STATEMENTS ------------ 

class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        super().__init__()
        self.expr = expr

class Declaration(Stmt):
    def __init__(self, ident: Token, expr: Expr):
        self.ident = ident
        self.expr = expr

class Assignment(Stmt):
    def __init__(self, left: Expr, expr: Expr):
        self.left = left
        self.expr = expr

class Return(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

class Block(Stmt):
    def __init__(self, stmts: list[Stmt]):
        self.stmts = stmts

# ----------- EXPRESSIONS ------------

class Empty(Expr):
    pass

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
        self.inner = inner

class Binary(Expr):
    def __init__(self, left: Expr, right: Expr, op: Token):
        super().__init__()
        self.left = left
        self.right = right
        self.op = op

class Unary(Expr):
    def __init__(self, expr: Expr, op: Token):
        self.expr = expr
        self.op = op

class Args(Expr):
    def __init__(self, args: list[Expr]):
        self.args = args

class Call(Expr):
    def __init__(self, callee: Expr, inner: Expr):
        self.callee = callee
        self.inner = inner
