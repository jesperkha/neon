from tokens import *
import ast
import util

def scan_tree(tree: ast.AstNode):
    Scanner(tree).scan()

class Type:
    def __init__(self, typ: str, kind: str) -> None:
        self.kind     = kind
        self.type_num = typ
        self.type_str = ""

class Scanner:
    def __init__(self, tree: ast.AstNode) -> None:
        self.tree = tree
        self.def_stack = [{}]

    def scan(self):
        for stmt in self.tree.stmts:
            self.scan_stmt(stmt)

    def scan_stmt(self, stmt: ast.Stmt) -> Type:
        t = type(stmt)

        if t == ast.ExprStmt:
            return self.scan_expr(stmt.expr)

        util.err(f"scanning for {stmt.__class__.__name__} not implemented")

    def scan_expr(self, expr: ast.Expr) -> Type:
        t = type(expr)

        if t == ast.Literal:
            k = expr.token.kind
            if k == KIND_NONE:
                return Type(TYPE_NULL, KIND_NONE)

            if k == KIND_BOOL:
                return Type(TYPE_BOOL, KIND_BOOL)

            if k == KIND_STRING:
                typ = TYPE_STRING if expr.token.type == STRING else TYPE_CHAR
                return Type(typ, KIND_STRING)
            
            if k == KIND_NUMBER:
                pass

            if k == KIND_ARRAY:
                pass

            if k == KIND_STRUCT:
                pass

        util.err(f"scanning for {expr.__class__.__name__} not implemented")

    def push(self):
        pass

    def pop(self):
        pass

    def get(self, name: str) -> any:
        pass