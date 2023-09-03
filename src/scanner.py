from tokens import *
import ast
import util

def scan_tree(tree: ast.AstNode):
    Scanner(tree).scan()

class Type:
    def __init__(self, typ: str, kind: str) -> None:
        self.kind = kind
        self.type = typ
        self.type_str = ""

class Scanner:
    def __init__(self, tree: ast.AstNode) -> None:
        self.tree = tree
        self.def_stack = [{}]

        self.errstack = util.ErrorStack()

    def err(self, msg: str, node):
        self.errstack.add(util.Error(msg, node.line, node.start, node.stop, node.string, True))

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
                typ = TYPE_F32 if expr.token.isfloat else TYPE_I32
                return Type(typ, KIND_NUMBER)
            
            if k == KIND_ARRAY:
                util.err("scanning for array not implemented")

            if k == KIND_STRUCT:
                util.err("scanning for struct not implemented")

        if t == ast.Binary:
            left = self.scan_expr(expr.left)
            right = self.scan_expr(expr.right)

            match_type = left.type == right.type
            match_kind = left.kind == right.kind
            op = expr.op.type
            kind = left.kind

            # Number operations
            # Todo: scanning for binary op
            if match_kind and kind == KIND_NUMBER:
                if op in (PLUS, MINUS, STAR, SLASH):
                    if not match_type:
                        self.err("unmatched types in expression", expr)
                    
                    return Type(left.type, kind)

        util.err(f"scanning for {expr.__class__.__name__} not implemented")

    def push(self):
        pass

    def pop(self):
        pass

    def get(self, name: str) -> any:
        pass