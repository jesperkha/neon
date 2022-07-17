# Scanner
import util
from tokens import *

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
    # Todo: create map for statement/expression type to handler
    def scan(self):
        for stmt in self.ast:
            self.scan_stmt(stmt)

    # Declare new variable to current scope, throws an error if already declared.
    # Warns if a variable is being shadowed
    def declare(self, name: str, type: Type):
        if type == TYPE_FUNC and self.scope != 0:
            util.err(f"functions can only be declared at top level, line {self.line}")
        # Debug
        # if type != TYPE_FUNC and self.scope == 0:
        #     util.err(f"illegal statement at top level, line {self.line}")
        scope = self.scope_list[self.scope]
        if name in scope:
            util.err(f"'{name}' is already declared, line {self.line}")
        for i in range(self.scope):
            if name in self.scope_list[i]:
                warn(f"variable shadowing of '{name}', line {self.line}")
        scope[name] = type

    # Does not assign a value but checks if the variable is defined and that the
    # type matches the original value.
    def assign(self, name: str, type: Type):
        scope = self.scope_list[self.scope]
        if name not in scope:
            util.err(f"'{name}' must be declared before assignment, line {self.line}")

        prev = scope[name]
        if prev != type:
            util.err(f"mismatched types in assignment, expected {prev}, got {type}, line {self.line}")
        scope[name] = type
    
    # Gets variable type from lookup. Iterates through scope list backwards
    def get_var(self, name: str) -> Type:
        i = self.scope
        while i > -1:
            scope = self.scope_list[i]
            if name in scope:
                return scope[name]
            i -= 1
        util.err(f"'{name}' is undefined, line {self.line}")

    # Pushes into new scope
    def push_scope(self):
        self.scope += 1
        self.scope_list.append({})
    
    # Pops scope
    def pop_scope(self):
        self.scope -= 1
        self.scope_list.pop()

    # Scans a single statement
    def scan_stmt(self, stmt: Statement):
        if stmt.type == STMT_EXPR:
            eval_expr(stmt.expr, self.line)

    def scan_stmt_none(self):
        util.err(f"invalid statement, line {self.line}")

    def scan_stmt_expr(self):
        eval_expr(stmt.expr, self.line)

    def scan_stmt_declare(self):
        expr_type = eval_expr(stmt.expr, self.line)
        self.declare(stmt.name.lexeme, expr_type)
        if stmt.vtype:
            def_type = stmt.vtype
            if expr_type != def_type:
                util.err(f"mismatched types in assignment, expected {def_type}, got {expr_type}, line {self.line}")
        else: # colon equal declaration
            stmt.vtype = expr_type

    def scan_stmt_assign(self):
        self.assign(stmt.name.lexeme, eval_expr(stmt.expr, self.line), self.line)

    def scan_stmt_func(self):
        pass

    def scan_stmt_print(self):
        pass

    def scan_stmt_block(self):
        pass

    def scan_stmt_return(self):
        pass


# Evaluates an expression and returns the evaluated type and error (None)
def eval_expr(expr: Expression, line: int) -> Type:
    # Todo: figure out how to store/pass state
    if expr.type == EXPR_VARIABLE:
        return self.get_var(expr.tokens[0].lexeme)

    elif expr.type == EXPR_EMPTY:
        return Type(TYPE_NONE)

    elif expr.type == EXPR_GROUP:
        return eval_expr(expr.inner, line)

    elif expr.type == EXPR_ARGS:
        # args is parsed manually by statements and expressions that use it
        # other instances are errors
        util.err(f"unexpected argument list, line {line}")

    # Todo: scan call expression
    elif expr.type == EXPR_CALL:
        pass

    elif expr.type == EXPR_UNARY:
        right = eval_expr(expr.right, line)
        op = expr.operator
        if op.type in (MINUS, BIT_NEGATE):
            if right.kind != KIND_NUMBER:
                util.err(f"invalid operator '{op}' for type {right}, line {line}")
            return right
        if right.kind != KIND_BOOL:
            util.err(f"invalid operator '{op}' for type {right}, line {line}")
        return Type(TYPE_BOOL) # NOT operator

    elif expr.type == EXPR_ARRAY:
        if expr.inner.type == EXPR_ARGS:
            types = [eval_expr(typ, line) for typ in expr.inner.exprs]
            inner_t = types[0]
            for idx, t in enumerate(types):
                if t != inner_t:
                    util.err(f"type of index {idx} did not match the first element in array literal; expected {inner_t}, got {t}, line {line}")
            return Type(TYPE_ARRAY, sub_type=inner_t)

        inner_t = eval_expr(expr.inner, line)
        return Type(TYPE_ARRAY, sub_type=inner_t)

    elif expr.type == EXPR_INDEX:
        arr = eval_expr(expr.array, line)
        if arr != TYPE_ARRAY:
            util.err(f"type {arr.type} is not indexable, line {line}")

        index = eval_expr(expr.inner, line)
        if index not in COLLECTION_UNSIGNED:
            util.err(f"expected index to be integer, got {index}, line {line}")

        # Todo: handle negative indexing
        # Todo: check index out of range
        return arr.sub_t

    elif expr.type == EXPR_LITERAL:
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

    elif expr.type == EXPR_BINARY:
        left  = eval_expr(expr.left, line)
        right = eval_expr(expr.right, line)
        op = expr.operator
        
        # Todo: implement the remaining ops
        if op.type == IN:
            if right != TYPE_ARRAY:
                util.err(f"expected right expression to be array, got {right}, line {line}")
            if left != right.sub_t:
                util.err(f"left expression did not match array type; expected {right.sub_t}, got {left}, line {line}") 
            return Type(TYPE_BOOL)

        for n in (left, right): # check operator
            if op.type not in binary_op_combos[n.kind]:
                util.err(f"invalid operator '{op}' for type {n}, line {line}")

        if op.type in (BIT_OR, BIT_XOR, BIT_AND, BIT_LSHIFT, BIT_RSHIFT):
            if op.type in (BIT_LSHIFT, BIT_RSHIFT):
                # check if right is unsigned int
                if right.type not in COLLECTION_UNSIGNED:
                    util.err(f"expected unsigned int in shift expression, got {right}, line {line}")
                return left
            
            # Todo: check for bit length of number
            # Todo: add runtime err for negative numbers
            return left

        if op.type == MODULO:
            if right.type not in COLLECTION_UNSIGNED:
                util.err(f"expected unsigned int in modulo expression, got {right}, line {line}")
            return Type(TYPE_INT)

        if right == TYPE_ARRAY or left == TYPE_ARRAY:
            # Matches array and value types, raises error on mismatch
            e = "new element does not match the array type; expected {}, got {}, line {}"
            if right == TYPE_ARRAY and left != TYPE_ARRAY:
                if right.sub_t != left:
                    util.err(e.format(right.sub_t, left, line))
                return right

            if right != TYPE_ARRAY and left == TYPE_ARRAY:
                if left.sub_t != right:
                    util.err(e.format(left.sub_t, right, line))
                return left

            if left.sub_t != right.sub_t:
                util.err(f"mismatched array types in expression; {left.sub_t} and {right.sub_t}, line {line}")
            return left

        if left == right:
            return left

        util.err(f"mismatched types {left} and {right} in expression, line {line}")
