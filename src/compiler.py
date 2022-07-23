from tokens import *
import util

type_convertion = {
        "STRING": "char*",
        "NONE": "void",
        "BOOL": "bool",
        "I32": "int",
        "F32": "float"
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
        self.stmts(ast)
        return self.str()

    def stmts(self, ast: list[Statement]):
        for stmt in ast:
            self.indent_line()
            self.stmt(stmt)

        self.newline()

    def stmt(self, stmt: Statement):
        t = stmt.type

        if t == STMT_FUNC:
            self.type(stmt.vtype)
            self.name(stmt.name)
            self.params(stmt.params)
            self.brace_start()
            self.stmts(stmt.block.stmts)
            self.brace_end()
            return

        if t == STMT_EXPR:
            self.expr(stmt.expr)
            self.semicolon()
            return

        if t == STMT_RETURN:
            self.add("return")
            self.expr(stmt.expr)
            self.semicolon()
            return

        if t == STMT_DECLARE:
            self.type(stmt.vtype)
            self.name(stmt.name)
            self.add("=")
            self.expr(stmt.expr)
            self.semicolon()
            return
        
        if t == STMT_ASSIGN:
            self.name(stmt.name)
            self.add("=")
            self.expr(stmt.expr)
            self.semicolon()
            return

        util.err(f"compilation for {t} not implemented, line {stmt.line}")

    def expr(self, expr: Expression):
        t = expr.type

        if t == EXPR_EMPTY:
            return

        if t == EXPR_ARGS:
            for e in expr.exprs:
                self.expr(e)
                self.string += ","
            if len(expr.exprs) > 0:
                self.pop()
            return
        
        if t == EXPR_LITERAL:
            self.name(expr.tokens[0])
            return

        if t == EXPR_VARIABLE:
            self.name(expr.tokens[0])
            return
        
        if t == EXPR_UNARY:
            self.symbol(expr.operator, True)
            self.expr(expr.right)
            return

        if t == EXPR_CALL:
            self.name(expr.callee)
            self.paren_start()
            self.expr(expr.inner)
            self.paren_end()
            return

        if t == EXPR_ARRAY:
            self.add("[")
            self.add("]")
            return
                
        util.err(f"compiling for {t} is not implemented")


    def str(self) -> str:
        return self.string[1:]
    
    def autospace(func):
        def wrap(self, s):
            for n in range(self.spaces):
                self.string += " "

            func(self, s)
            self.spaces = 1
            
        return wrap

    # Recursives

    def pop(self):
        self.string = self.string[:-1]
        
    def indent_line(self, change: int = 0):
        self.indent += change
        for n in range(self.indent):
           self.string += "\t"
        
    def symbol(self, sym: Token, unary: bool = False):
        if sym.lexeme in symbol_convertion:
            self.add(symbol_convertion[sym.lexeme])
        else:
            self.name(sym)
        if unary:
            self.spaces = 0
        
    @autospace
    def add(self, s: str):
        if type(s) == Compiler:
            self.string += s.str()
        else:
            self.string += s
            
    @autospace
    def type(self, typ: Type, reference: bool = False):
        if typ.type in type_convertion:
            self.string += type_convertion[typ.type]
        elif typ.type == TYPE_ARRAY:
            self.type(typ.sub_type)
            self.string += typ.ctype
        else:
            self.string += f"ne_{typ}_t"
        
    @autospace
    def name(self, name: Token):
        self.string += name.lexeme
        
    def newline(self):
        self.string += "\n"
        self.spaces = 0
        
    def semicolon(self):
        self.string += ";"
        self.newline()
            
    def paren_start(self):
        self.string += "("
        self.spaces = 0
        
    def paren_end(self):
        self.string += ")"
        
    def brace_start(self):
        self.indent_line()
        self.newline()
        self.add("{")
        self.newline()
        self.indent += 1
        
    def brace_end(self):
        self.pop() # remove additional newline
        self.indent_line(-1)
        self.spaces = 0
        self.add("}")
        self.newline()
        self.newline()
        
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
        
