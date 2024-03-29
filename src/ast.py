from tokens import *

class Type:
    def __init__(self, typ: str, user_def: bool = False) -> None:
        self.type = typ
        self.user_def = user_def
        self.string = typ
        if not user_def:
            self.kind = type_to_kind[typ]
        else:
            self.kind = KIND_NONE

class Param:
    def __init__(self, name: str, typ: Type):
        self.name = name
        self.type = typ

class AstNode:
    def __init__(self):
        self.stmts = []
        self.indent = 0

    # Todo: rewrite syntax tree print function
    def print(self):
        for node in self.stmts:
            self.indent = -1
            if s := self.string_node(node):
                print(s)

    def print_block(self, block):
        for node in block.stmts:
            s = self.string_node(node)
            print(s, end="" if s == "" else "\n")

    def concat(self, title: str, suffix: str, end: str = "\n") -> str:
        if suffix == "": end = ""
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
            if type(node.expr) == Empty:
                return ""
            return self.concat("ExprStmt", self.string_node(node.expr))

        elif t == Block:
            print(self.concat("Block", "", ""))
            self.print_block(node)
            return ""

        elif t == Function:
            s = ""
            for p in node.params:
                s += f"{p.name}: {p.type.string}, "
            s = "(" + s[:len(s)-2] + ")"
            if node.return_t:
                s += f": {node.return_t.string}"

            func = self.concat(f"Function {node.name}", s, "")
            print(func)
            self.print_block(node.body)
            return ""

        elif t == If:
            print(self.concat("If", "", ""))
            print(self.concat(".expr", self.string_node(node.expr)))
            print(".block:")
            self.print_block(node.block)
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
            left  = self.concat(".left", self.string_node(node.left))
            right = self.concat(".right", self.string_node(node.right))
            op    = self.concat(".op", node.op.lexeme, "")
            self.indent -= 1
            return self.concat("Binary", f"{op}\n{left}\n{right}")

        elif t == Unary:
            self.indent += 1
            op   = self.concat("op", node.op.lexeme, "")
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
            inner  = self.concat(".inner", self.string_node(node.inner))
            self.indent -= 1
            return self.concat("Call", f"{callee}\n{inner}")

        return ""

class ParseNode:
    def __init__(self, *args):
        self.signature = Signature(self)
        for a in args:
            self.signature.add(a)
        self.type = None
        self.line = 0
        self.start = 0
        self.stop = 0
        self.string = ""

class Stmt(ParseNode):
    def __init__(self, *args):
        super().__init__(*args)

class Expr(ParseNode):
    def __init__(self, *args):
        super().__init__(*args)

# ------------ STATEMENTS ------------ 

class ExprStmt(Stmt):
    def __init__(self, expr: Expr):
        super().__init__(expr)
        self.expr = expr

class Declaration(Stmt):
    def __init__(self, ident: Token, expr: Expr):
        super().__init__(ident, expr)
        self.ident = ident
        self.expr = expr

class Assignment(Stmt):
    def __init__(self, left: Expr, expr: Expr):
        super().__init__(left, expr)
        self.left = left
        self.expr = expr

class Return(Stmt):
    def __init__(self, expr: Expr):
        super().__init__(expr)
        self.expr = expr

class Block(Stmt):
    def __init__(self, stmts: list[Stmt]):
        super().__init__(stmts)
        self.stmts = stmts

class Function(Stmt):
    def __init__(self, name: str, params: list[Param], return_t: Type, body: Block):
        super().__init__(name, params, return_t, body)
        self.name = name
        self.params = params
        self.return_t = return_t
        self.body = body

class If:
    def __init__(self, expr: Expr, block: Block) -> None:
        super().__init__(expr, block)
        self.expr = expr
        self.block = block

# ----------- EXPRESSIONS ------------

def is_empty(expr: Expr) -> bool:
    return type(expr) == type(Empty())

class Empty(Expr):
    pass

class Literal(Expr):
    def __init__(self, tok: Token):
        super().__init__(tok)
        self.token = tok

class Variable(Expr):
    def __init__(self, tok: Token):
        super().__init__(tok)
        self.token = tok

class Group(Expr):
    def __init__(self, inner: Expr):
        super().__init__(inner)
        self.inner = inner

class Binary(Expr):
    def __init__(self, left: Expr, right: Expr, op: Token):
        super().__init__(left, right, op)
        self.left = left
        self.right = right
        self.op = op

class Unary(Expr):
    def __init__(self, expr: Expr, op: Token):
        super().__init__(expr, op)
        self.expr = expr
        self.op = op

class Args(Expr):
    def __init__(self, args: list[Expr]):
        super().__init__(args)
        self.args = args

class Call(Expr):
    def __init__(self, callee: Expr, inner: Expr):
        super().__init__(callee, inner)
        self.callee = callee
        self.inner = inner

