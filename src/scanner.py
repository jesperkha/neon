# Scanner
from tokens import *
from util import *

class scanner:
    def __init__(self, ast: list[Statement]) -> None:
        self.ast = ast
        self.line = 0

        # set after checking a function, used for
        # checking expression in returns
        self.return_type = Type(TYPE_NONE)

        for s in self.ast:
            self.scan(s)

    def scan(self, stmt: Statement):
        t = stmt.type
        self.line = stmt.line
        if t == STMT_NONE:
            err("invalid statement")

        elif t == STMT_PRINT:
            if stmt.expr.type in (EXPR_EMPTY, EXPR_ARGS):
                err(f"expected expression after print, line {self.line}")

        elif t == STMT_FUNC:
            self.return_type = stmt.vtype
        
        elif t == STMT_RETURN:
            typ = self.check_expr(stmt.expr)
            if self.compare_type(typ, self.return_type):
                err(f"incorrect return type, expected '{self.return_type.str()}', line {self.line}")
    
    # Evaluates expression and checks for unmatched types, undefined variables etc
    # Returns the expressions evaluated type
    # Todo: implement expr check
    def check_expr(self, expr: Expression) -> Type:
        pass
    
    # Returns true if types of both expressions are the same
    def compare_type(self, a: Type, b: Type) -> bool:
        return a.str() == b.str()