# Scanner
from tokens import *
from util import *

def scan(ast: list[Statement]):
    scanner(ast).scan()

class scanner:
    def __init__(self, ast: list[Statement]):
        self.ast = ast
        self.line = 0
        # set after checking a function, used for
        # checking expression in returns
        self.return_type = TYPE_NONE

        # List of dicts to indicate scopes. Higher idx is
        # higher scope. Pops the scope after exiting
        self.scope = 0
        self.scope_list = [{}]

    # Scans entire AST, returns nothing, raises error at first fault.
    def scan(self):
        idx = 0
        while idx < len(self.ast):
            stmt = self.ast[idx]
            self.scan_stmt(stmt)
            idx += 1
    
    # Scans block statement while keeping scanner state
    def scan_block(self, block: Statement):
        self.push_scope()
        for s in block.stmts:
            self.scan_stmt(s)
        self.pop_scope()

    # Scans a single statement, dependent on current state of scanner
    def scan_stmt(self, stmt: Statement):
        self.line = stmt.line
        t = stmt.type

        if t == STMT_NONE:
            err(f"invalid statement, line {self.line}")
        elif t == STMT_DECLARE:
            expr_type = self.eval_expr(stmt.expr)
            def_type  = stmt.vtype.str()
            if expr_type != def_type:
                err(f"incompatible types in assignment, expected {def_type}, got {expr_type}, line {self.line}")
            self.declare(stmt.name.lexeme, expr_type)
        elif t == STMT_ASSIGN:
            self.assign(stmt.name.lexeme, self.eval_expr(stmt.expr))
    
    # Evaluates expression and checks for unmatched types, undefined variables etc
    # Returns the expressions evaluated type
    def eval_expr(self, expr: Expression, allow_empty: bool = False) -> str:
        return TYPE_NONE
    
    # Declare new variable to current scope, throws an error if already declared.
    # Warns if a variable is being shadowed
    def declare(self, name: str, type: str):
        if type == TYPE_FUNC and self.scope != 0:
            err(f"functions can only be declared at top level, line {self.line}")
        # elif type != TYPE_FUNC and self.scope == 0:
        #     err(f"illegal statement at top level, line {self.line}")
        scope = self.scope_list[self.scope]
        if name in scope:
            err(f"'{name}' is already declared, line {self.line}")
        for i in range(self.scope):
            if name in self.scope_list[i]:
                warn(f"variable shadowing of '{name}', line {self.line}")
        scope[name] = type

    # Does not assign a value but checks if the variable is defined and that the
    # type matches the original value.
    def assign(self, name: str, type: str):
        scope = self.scope_list[self.scope]
        if name not in scope:
            err(f"variable '{name}' must be declared before assignment, line {self.line}")
        prev = scope[name]
        if prev != type:
            err(f"incompatible types in assignment, expected {prev}, got {type}, line {self.line}")
        scope[name] = type

    # Pushes into new scope
    def push_scope(self):
        self.scope += 1
        self.scope_list.append({})
    
    # Pops scope
    def pop_scope(self):
        self.scope -= 1
        self.scope_list.pop()