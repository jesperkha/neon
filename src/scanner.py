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
            self.declare(stmt.name.lexeme, expr_type)
            if stmt.vtype:
                def_type = stmt.vtype
                if expr_type != def_type:
                    err(f"incompatible types in assignment, expected {def_type}, got {expr_type}, line {self.line}")
            else: # colon equal declaration
                stmt.vtype = expr_type

        elif t == STMT_ASSIGN:
            self.assign(stmt.name.lexeme, self.eval_expr(stmt.expr))
        
        else: # Debug
            err(f"scanning for {t} is not implemented yet")
    
    # Evaluates expression and checks for unmatched types, undefined variables etc
    # Returns the expressions evaluated type
    def eval_expr(self, expr: Expression) -> Type:
        t = expr.type
        if t == EXPR_VARIABLE:
            return self.get_var(expr.tokens[0].lexeme)
        elif t == EXPR_LITERAL:
            if expr.tokens[0].isfloat:
                return Type(TYPE_FLOAT)
            return Type(TYPE_INT)

        return Type(TYPE_NONE)
    
    # Declare new variable to current scope, throws an error if already declared.
    # Warns if a variable is being shadowed
    def declare(self, name: str, type: Type):
        if type == TYPE_FUNC and self.scope != 0:
            err(f"functions can only be declared at top level, line {self.line}")
        # Debug
        # if type != TYPE_FUNC and self.scope == 0:
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
    def assign(self, name: str, type: Type):
        scope = self.scope_list[self.scope]
        if name not in scope:
            err(f"variable '{name}' must be declared before assignment, line {self.line}")

        prev = scope[name]
        if prev != type:
            err(f"incompatible types in assignment, expected {prev}, got {type}, line {self.line}")
        scope[name] = type
    
    # Gets variable type from lookup. Iterates through scope list backwards
    def get_var(self, name: str) -> Type:
        i = self.scope
        while i > -1:
            scope = self.scope_list[i]
            if name in scope:
                return scope[name]
            i -= 1
        err(f"'{name}' is undefined, line {self.line}")

    # Pushes into new scope
    def push_scope(self):
        self.scope += 1
        self.scope_list.append({})
    
    # Pops scope
    def pop_scope(self):
        self.scope -= 1
        self.scope_list.pop()