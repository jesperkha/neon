# Scanner
from sre_constants import LITERAL
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
        
        elif t == STMT_EXPR:
            self.eval_expr(stmt.expr)

        elif t == STMT_DECLARE:
            expr_type = self.eval_expr(stmt.expr)
            self.declare(stmt.name.lexeme, expr_type)
            if stmt.vtype:
                def_type = stmt.vtype
                if expr_type != def_type:
                    err(f"mismatched types in assignment, expected {def_type}, got {expr_type}, line {self.line}")
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
        
        elif t == EXPR_EMPTY:
            return Type(TYPE_NONE)
        
        elif t == EXPR_GROUP:
            return self.eval_expr(expr.inner)

        elif t == EXPR_LITERAL:
            tok = expr.tokens[0]
            if tok.type == STRING:
                return Type(TYPE_STRING)
            if tok.type == CHAR:
                return Type(TYPE_CHAR)
            if tok.type in (TRUE, FALSE):
                return Type(TYPE_BOOL)
            if tok.isfloat:
                return Type(TYPE_FLOAT)
            return Type(TYPE_INT)
        
        elif t == EXPR_ARRAY:
            if expr.inner.type == EXPR_ARGS:
                types = [self.eval_expr(typ) for typ in expr.inner.exprs]
                inner_t = types[0]
                for idx, t in enumerate(types):
                    if t != inner_t:
                        err(f"type of index {idx} did not match the first element in array literal; expected {inner_t}, got {t}, line {self.line}")
                return Type(TYPE_ARRAY, sub_type=inner_t)

            inner_t = self.eval_expr(expr.inner)
            return Type(TYPE_ARRAY, sub_type=inner_t)

        elif t == EXPR_UNARY:
            right = self.eval_expr(expr.right)
            op = expr.operator
            if op.type in (MINUS, BIT_NEGATE):
                if right.kind != KIND_NUMBER:
                    err(f"invalid operator '{op}' for type {right}, line {self.line}")
                return right
            if right.kind != KIND_BOOL:
                err(f"invalid operator '{op}' for type {right}, line {self.line}")
            return Type(TYPE_BOOL) # NOT operator
        
        elif t == EXPR_BINARY:
            left  = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            return self.check_binary_types(expr.operator, left, right)
        
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
            err(f"'{name}' must be declared before assignment, line {self.line}")

        prev = scope[name]
        if prev != type:
            err(f"mismatched types in assignment, expected {prev}, got {type}, line {self.line}")
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

    # Matches two type kinds, raises error on mismatch
    # Todo: implement the remaining ops
    def check_binary_types(self, op: Token, left: Type, right: Type) -> Type:
        for n in (left, right): # check operator
            if op.type not in binary_op_combos[n.kind]:
                err(f"invalid operator '{op}' for type {n}, line {self.line}")

        if right == TYPE_ARRAY or left == TYPE_ARRAY:
            return self.check_array_types(left, right)

        if left == right: return left
        err(f"mismatched types {left} and {right} in expression, line {self.line}")

    # Matches array and value types, raises error on mismatch
    def check_array_types(self, left: Type, right: Type) -> Type:
        e = "new element does not match the array type; expected {}, got {}, line {}"
        if right == TYPE_ARRAY and left != TYPE_ARRAY:
            if right.sub_t != left: err(e.format(right.sub_t, left, self.line))
            return right

        if right != TYPE_ARRAY and left == TYPE_ARRAY:
            if left.sub_t != right: err(e.format(left.sub_t, right, self.line))
            return left

        if left.sub_t != right.sub_t:
            err(f"mismatched array types in expression; {left.sub_t} and {right.sub_t}, line {self.line}")
        return left