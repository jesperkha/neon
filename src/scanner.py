# Scanner
import util
from tokens import *

def scan(ast: list[Statement]):
    scanner().scan(ast)

class Variable:
    def __init__(self, name: str, typ: Type, line: int):
        self.name = name
        self.type = typ
        self.used = False
        self.line = line

class Function:
    def __init__(self, name: str, return_t: Type, params: list, body: list[Statement]):
        self.name = name
        self.return_t = return_t
        self.params = params
        self.body = body

class scanner:
    def __init__(self):
        self.line = 0
        # set after checking a function, used for
        # checking expression in returns
        self.return_type = Type(TYPE_NONE)
        # -1 if false, other number for the scope. the
        # scope must be the same as the function
        self.returned = -1
        self.in_func = False

        # List of dicts to indicate scopes. Higher idx is
        # higher scope. Pops the scope after exiting
        self.scope = 0
        self.scope_list = [{}]

        # Global declarations
        self.dec_funcs = {}
        self.dec_structs = {}

        self.handlers = {
                STMT_EXPR: self.scan_stmt_expr,
                STMT_ASSIGN: self.scan_stmt_assign,
                STMT_BLOCK: self.scan_stmt_block,
                STMT_DECLARE: self.scan_stmt_declare,
                STMT_FUNC: self.scan_stmt_func,
                STMT_NONE: self.scan_stmt_none,
                STMT_RETURN: self.scan_stmt_return,
        }

    # Scans entire AST, returns nothing, raises error at first fault.
    def scan(self, statements: list[Statement]):
        for stmt in statements:
            self.line = stmt.line
            if stmt.type not in self.handlers:
                util.err(f"unknown statement type: {stmt.type}")

            top_level = (STMT_FUNC)
            if stmt.type in top_level and self.scope != 0:
                util.err(f"{stmt.type.lower()}s can only be declared at top level, line {self.line}")
            # Debug: allow top level variables for testing
            #if stmt.type not in top_level and self.scope == 0:
               #util.err(f"illegal statement at top level, line {self.line}")
                
            self.handlers[stmt.type](stmt)

        # Scan function bodies after global pass
        if self.scope == 0:
            for _, f in self.dec_funcs.items():
                self.scan_function_body(f)

    # Verifies types and returns the default type for types such as int (i32), float (f32) etc
    def validate_type(self, typ: Type) -> Type:
        if typ == TYPE_USRDEF:
            util.err(f"debug: userdef types not implemented yet, line {self.line}")
        elif typ == TYPE_INT:
            typ = Type(TYPE_I32)
        elif typ == TYPE_FLOAT:
            typ = Type(TYPE_F32)
        elif typ == TYPE_ARRAY:
            if typ.sub_type == TYPE_INT:
                typ.sub_type = Type(TYPE_I32)
            elif typ.sub_type == TYPE_FLOAT:
                typ.sub_type = Type(TYPE_F32)

        return typ

    # Returns true if variable is defined
    def is_defined(self, name: str, scope: dict = None) -> bool:
        s = self.scope_list[self.scope] if not scope else scope
        for _, v in s.items():
            if v.name == name:
                return True
        return False

    # Declare new variable to current scope, throws an error if already declared.
    # Warns if a variable is being shadowed
    def declare(self, name: str, typ: Type):
        # Declaration errors
        if name in keyword_lookup or name in typeword_lookup:
            util.err(f"keywords cannot be used as variable names, line {self.line}")
        if not typ:
            util.err(f"cannot assign null to a variable, line {self.line}")

        scope = self.scope_list[self.scope]
        if self.is_defined(name, scope):
            util.err(f"'{name}' is already declared, line {self.line}")
        for i in range(self.scope):
            if self.is_defined(name, self.scope_list[i]):
                util.warn(f"variable shadowing of '{name}', line {self.line}")

        scope[name] = Variable(name, typ, self.line)

    # Does not assign a value but checks if the variable is defined and that the
    # type matches the original value.
    def assign(self, name: str, typ: Type):
        i = self.scope
        while i > -1:
            scope = self.scope_list[i]
            if self.is_defined(name, scope):
                prev = scope[name].type
                if prev != typ:
                    util.err(f"mismatched types in assignment, expected {prev}, got {typ}, line {self.line}")
                # Todo: implement array length state
                scope[name].type = typ # Update array length
                return
            i -= 1

        util.err(f"'{name}' must be declared before assignment, line {self.line}")
    
    # Gets variable type from lookup. Iterates through scope list backwards
    def get_var(self, name: str) -> Type:
        i = self.scope
        while i > -1:
            scope = self.scope_list[i]
            if self.is_defined(name, scope):
                var = scope[name]
                var.used = True
                return var.type
            i -= 1
        util.err(f"'{name}' is undefined, line {self.line}")
    
    # Returns the param list from function definition
    def get_func(self, name: str) -> list:
        if name not in self.dec_funcs:
            util.err(f"function '{name}' is not defined, line {self.line}")

        return self.dec_funcs[name]

    # Pushes into new scope
    def push_scope(self):
        self.scope += 1
        self.scope_list.append({})
    
    # Pops scope
    def pop_scope(self):
        # Todo: check for unused variables
        for _, v in self.scope_list[self.scope].items():
            if not v.used:
                util.warn(f"'{v.name}' is unused, line {v.line}")

        self.scope -= 1
        self.scope_list.pop()


    def scan_stmt_none(self, stmt: Statement):
        util.err(f"invalid statement, line {self.line}")

    def scan_stmt_expr(self, stmt: Statement):
        t = self.eval_expr(stmt.expr)

    def scan_stmt_declare(self, stmt: Statement):
        expr_type = self.eval_expr(stmt.expr)
        self.declare(stmt.name.lexeme, expr_type)
        if stmt.vtype:
            expect_t = self.validate_type(stmt.vtype)
            if expr_type != expect_t:
                util.err(f"mismatched types in assignment, expected {expect_t}, got {expr_type}, line {self.line}")
        else: # colon equal declaration
            stmt.vtype = expr_type

    def scan_stmt_assign(self, stmt: Statement):
        self.assign(stmt.name.lexeme, self.eval_expr(stmt.expr))

    def scan_stmt_func(self, stmt: Statement):
        return_t = self.validate_type(stmt.vtype)
        func = Function(stmt.name.lexeme, return_t, stmt.params, stmt.block.stmts)
        self.dec_funcs[stmt.name.lexeme] = func

    def scan_function_body(self, func: Function):
        # Declare params to local scope
        self.push_scope()
        self.return_type = func.return_t
        self.in_func = True
        for name, typ in func.params:
            self.declare(name.lexeme, typ)

        # Check if function has returned if it should
        self.returned = -1
        func_scope = self.scope
        self.scan(func.body)
        if self.returned != func_scope and func.return_t:
            util.err(f"missing return in function '{func.name}', line {self.line}")

        self.in_func = False
        self.pop_scope()

    def scan_stmt_block(self, stmt: Statement):
        self.push_scope()
        self.scan(stmt.stmts)
        self.pop_scope()

    def scan_stmt_return(self, stmt: Statement):
        if not self.in_func:
            util.err(f"illegal return outside of function, line {self.line}")
        returned = self.eval_expr(stmt.expr)
        if returned != self.return_type:
            util.err(f"mismatched type in return, expected {self.return_type}, got {returned}, line {self.line}")

        self.returned = self.scope

    # Wrapper for the evaluation to return corrected types
    def eval_expr(self, expr: Expression) -> Type:
        return self.validate_type(self.eval_expr_wrap(expr))

    # Evaluates an expression and returns the evaluated type
    def eval_expr_wrap(self, expr: Expression) -> Type:
        if expr.type == EXPR_VARIABLE:
            return self.get_var(expr.tokens[0].lexeme)

        elif expr.type == EXPR_EMPTY:
            return Type(TYPE_NONE)

        elif expr.type == EXPR_GROUP:
            return self.eval_expr(expr.inner)

        elif expr.type == EXPR_ARGS:
            # args is parsed manually by statements and expressions that use it
            # other instances are errors
            util.err(f"unexpected argument list, line {self.line}")

        elif expr.type == EXPR_CALL:
            func = self.get_func(expr.callee.lexeme)
            args = expr.inner

            arg_list = []
            if args.type not in (EXPR_ARGS, EXPR_EMPTY):
                arg_list = [self.eval_expr(args)]
            elif args.type != EXPR_EMPTY:
                for e in args.exprs:
                    arg_list.append(self.eval_expr(e))

            if len(arg_list) != len(func.params):
                util.err(f"'{func.name}' takes {len(func.params)} arguments, got {len(arg_list)}, line {self.line}")

            for idx, arg in enumerate(arg_list):
                name, typ = func.params[idx]
                if arg != typ:
                    util.err(f"argument {idx+1} in '{func.name}' expects type {typ}, got {arg}, line {self.line}")

            return func.return_t

        elif expr.type == EXPR_UNARY:
            right = self.eval_expr(expr.right)
            op = expr.operator
            if op.type in (MINUS, BIT_NEGATE):
                if right.kind != KIND_NUMBER:
                    util.err(f"invalid operator '{op}' for type {right}, line {self.line}")
                right.negative = not right.negative
                return right
            if right.kind != KIND_BOOL:
                util.err(f"invalid operator '{op}' for type {right}, line {self.line}")
            return Type(TYPE_BOOL) # NOT operator

        elif expr.type == EXPR_ARRAY:
            if expr.inner.type == EXPR_ARGS:
                types = [self.eval_expr(typ) for typ in expr.inner.exprs]
                inner_t = types[0]
                for idx, t in enumerate(types):
                    if t != inner_t:
                        util.err(f"type of index {idx} did not match the first element in array literal; expected {inner_t}, got {t}, line {self.line}")
                return Type(TYPE_ARRAY, compl="[]", sub_type=inner_t)

            inner_t = self.eval_expr(expr.inner)
            return Type(TYPE_ARRAY, compl="[]", sub_type=inner_t, empty=inner_t==EXPR_EMPTY)

        elif expr.type == EXPR_INDEX:
            arr = self.eval_expr(expr.array)
            if arr != TYPE_ARRAY:
                util.err(f"type {arr.type} is not indexable, line {self.line}")

            index = self.eval_expr(expr.inner)
            if index.float:
                util.err(f"expected index to be integer, got {index}, line {self.line}")

            # Todo: handle negative indexing
            # Todo: check index out of range
            return arr.sub_type

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
            left  = self.eval_expr(expr.left)
            right = self.eval_expr(expr.right)
            op = expr.operator
            
            # Todo: implement the remaining ops
            if op.type == IN:
                if right != TYPE_ARRAY:
                    util.err(f"expected right expression to be array, got {right}, line {self.line}")
                if left != right.sub_type:
                    util.err(f"left expression did not match array type; expected {right.sub_type}, got {left}, line {self.line}") 
                return Type(TYPE_BOOL)

            for n in (left, right): # check operator
                if op.type not in binary_op_combos[n.kind]:
                    util.err(f"invalid operator '{op}' for type {n}, line {self.line}")

            # Todo: make function to check if number is signed/negative
            if op.type in (BIT_OR, BIT_XOR, BIT_AND, BIT_LSHIFT, BIT_RSHIFT):
                if op.type in (BIT_LSHIFT, BIT_RSHIFT):
                    # check if right is unsigned int
                    if right.type not in COLLECTION_UNSIGNED:
                        util.err(f"expected unsigned int in shift expression, got {right}, line {self.line}")
                    return left
                
                # Todo: check for bit length of number
                # Todo: add runtime err for negative numbers
                return left

            if op.type == MODULO:
                if right.type not in COLLECTION_UNSIGNED:
                    util.err(f"expected unsigned int in modulo expression, got {right}, line {self.line}")
                return Type(TYPE_INT)

            if right == TYPE_ARRAY or left == TYPE_ARRAY:
                # Matches array and value types, raises error on mismatch
                e = "new element does not match the array type; expected {}, got {}, line {}"
                if right == TYPE_ARRAY and left != TYPE_ARRAY:
                    if right.sub_type != left:
                        util.err(e.format(right.sub_type, left, self.line))
                    return right

                if right != TYPE_ARRAY and left == TYPE_ARRAY:
                    if left.sub_type != right:
                        util.err(e.format(left.sub_type, right, self.line))
                    return left

                if left != right:
                    util.err(f"mismatched array types in expression; {left} and {right}, line {self.line}")
                return left

            if left == right:
                return left

            util.err(f"mismatched types {left} and {right} in expression, line {self.line}")
