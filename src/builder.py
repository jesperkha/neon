from tokens import *
import ast
import util

def build(trees: list[ast.AstNode]) -> list[str]:
    return Builder(trees).build()

class Builder:
    def __init__(self, trees: list[ast.AstNode]) -> None:
        self.trees = trees
        self.indent = 0
    
    def build(self):
        files = []
        for tree in self.trees:
            file = ""
            for stmt in tree.stmts:
                file += self.stmt(stmt)
            
            files.append(file)

        return files

    def stmt(self, stmt: ast.Stmt) -> str:
        t = type(stmt)

        if t == ast.ExprStmt:
            return self.indent*"\t" + self.expr(stmt.expr)
        
        util.err(f"statement building for {stmt.__class__.__name__} not implemented")

    def expr(self, expr: ast.Expr) -> str:
        t = type(expr)

        if t == ast.Literal:
            return expr.token.lexeme
        
        util.err(f"expression building for {expr.__class__.__name__} not implemented")