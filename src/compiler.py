from tokens import *
import util

type_convertion = {
        "STRING": "char*",
        "NONE": "void",
        "INT": "int",
        "BOOL": "bool"
}

symbol_convertion = {
}

class Compiler:
    def __init__(self):
        self.declaration = False
        self.string = ""
        self.indent = 0
        self.spaces = 1

    def compile(self, ast: list[Statement]) -> str:
        return self.stmts(ast).str()

    def stmts(self, ast: list[Statement]):
        for stmt in ast:
            self.indent_line()
            self.stmt(stmt)

        return self.newline()

    def stmt(self, stmt: Statement):
        t = stmt.type

        if t == STMT_FUNC:
            return self \
                    .type(stmt.vtype) \
                    .name(stmt.name) \
                    .params(stmt.params) \
                    .brace_start() \
                    .stmts(stmt.block.stmts) \
                    .brace_end()

        elif t == STMT_EXPR:
            return self \
                    .expr(stmt.expr) \
                    .semicolon()

        elif t == STMT_RETURN:
            return self \
                    .add("return") \
                    .expr(stmt.expr) \
                    .semicolon()

        util.err(f"compilation for {t} not implemented, line {stmt.line}")

    def expr(self, expr: Expression):
        t = expr.type

        if t == EXPR_EMPTY:
            return self

        elif t == EXPR_ARGS:
            for e in expr.exprs:
                self.expr(e)
                self.string += ","
            if len(expr.exprs) > 0:
                self.pop()
            return self
        
        elif t == EXPR_LITERAL:
            return self.name(expr.tokens[0])

        elif t == EXPR_VARIABLE:
            return self.name(expr.tokens[0])
        
        elif t == EXPR_UNARY:
            return self \
                    .symbol(expr.operator, True) \
                    .expr(expr.right)

        elif t == EXPR_CALL:
            return self \
                    .name(expr.callee) \
                    .paren_start() \
                    .expr(expr.inner) \
                    .paren_end()
                
        util.err(f"compiling for {t} is not implemented")


    def str(self) -> str:
        return self.string[1:]
    
    def autospace(func):
        def wrap(self, s):
            for n in range(self.spaces):
                self.string += " "

            func(self, s)
            self.spaces = 1
            return self

        return wrap

    # Recursives

    def pop(self):
        self.string = self.string[:-1]
        return self

    def indent_line(self, change: int = 0):
        self.indent += change
        for n in range(self.indent):
           self.string += "\t"
        return self

    def symbol(self, sym: Token, unary: bool = False):
        if sym.lexeme in symbol_convertion:
            self.add(symbol_convertion[sym.lexeme])
        else:
            self.name(sym)
        if unary:
            self.spaces = 0
        return self

    @autospace
    def add(self, s: str):
        if type(s) == Compiler:
            self.string += s.str()
        else:
            self.string += s
        return self
    
    @autospace
    def type(self, typ: Type):
        if typ.type in type_convertion:
            self.string += type_convertion[typ.type]
        else:
            self.string += f"ne_{typ}_t"
        return self

    @autospace
    def name(self, name: Token):
        self.string += name.lexeme
        return self

    def newline(self):
        self.string += "\n"
        self.spaces = 0
        return self

    def semicolon(self):
        self.string += ";"
        self.newline()
        return self
    
    def paren_start(self):
        self.string += "("
        self.spaces = 0
        return self

    def paren_end(self):
        self.string += ")"
        return self

    def brace_start(self):
        self.indent_line()
        self.newline()
        self.add("{")
        self.newline()
        self.indent += 1
        return self

    def brace_end(self):
        self.pop() # remove additional newline
        self.indent_line(-1)
        self.spaces = 0
        self.add("}")
        self.newline()
        self.newline()
        return self

    def params(self, params):
        self.paren_start()
        for a in params:
            # Params
            self.type(a[1])
            self.name(a[0])
            self.string += ","

        if len(params) > 0:
            self.pop()

        self.paren_end()
        return self

