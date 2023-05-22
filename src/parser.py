from tokens import *
from ast import *
import util

class Parser:
    def __init__(self, tokens: list[Token]):
        self.errstack = util.ErrorStack()
        self.line = 1

        # Current token list that is being parsed. Expressions usually
        # have recursive calls so a token list stack gives depth without
        # recursion and creating multiple objects.
        self.list = [tokens]
        # List of indecies from token stack
        self.idxs = [0]
        # Index of current token list (always last)
        self.ptr = 0

        # Todo: implement definition scope and check variables/types

    # Parses token list. Returns AST. Exits on error
    def parse(self) -> AstNode:
        ast = AstNode()
        while self.idx < self.len:
            ast.stmts.append(self.stmt())

        self.errstack.print()
        return ast

    # Shorthand for invoking a procedure on a new stack frame
    def proc(self, tokens: list[Token], func) -> any:
        self.add(tokens)
        v = func()
        self.pop()
        return v

    # Parses single statement
    def stmt(self) -> Stmt:
        self.line = self.current.line
        t = self.current.type

        # Variable declaration
        if var := self.seek(COLON_EQUAL):
            if len(var) != 1 or var[0].type != IDENTIFIER:
                self.range_err("expected identifier on left side of ':='", var, True)

            expr = self.proc(self.seek(NEWLINE), self.expr)
            return Declaration(var[0], expr)

        # Assignment. Left side is expression in case of
        # indexing or struct property, checked in scan.
        if var := self.seek(EQUAL):
            left = self.proc(var, self.expr)
            expr = self.proc(self.seek(NEWLINE), self.expr)
            return Assignment(left, expr)

        # Return statement. Return outside func checked in scan.
        if t == RETURN:
            self.next()
            return Return(self.proc(self.seek(NEWLINE), self.expr))
        
        # Block statement
        if t == LEFT_BRACE:
            return self.block()

        # Function statement
        if t == FUNC:
            self.next() # skip keyword

            # Function name and left paren before params
            name = self.expect(IDENTIFIER, "function name")
            self.expect(LEFT_PAREN, "'('")

            # Consume all parameter names and types
            params = []
            while not self.eof and self.current.type != RIGHT_PAREN:
                name = self.expect(IDENTIFIER, "parameter name")
                params.append(Param(name.lexeme, self.type()))
                if self.current.type != COMMA:
                    self.expect(RIGHT_PAREN, "')'")
                    break

                self.next()

            # While statement only exits from break
            else: self.expect(RIGHT_PAREN, "')'")

            # Consumes possible return type
            return_t = None
            if self.current.type != LEFT_BRACE:
                return_t = self.type()

            # Function body as block statement
            block = self.block()
            return Function(name.lexeme, params, return_t, block)

        # Fallthrough is expression statement
        return ExprStmt(self.proc(self.seek(NEWLINE), self.expr))
    
    # Parses single block statement. Expects it, throws error if not found
    def block(self) -> Block:
        self.expect(LEFT_BRACE, "block")
        ast = self.proc(self.seek(RIGHT_BRACE), self.parse)
        return Block(ast.stmts)

    # Parses single expression
    def expr(self) -> Expr:
        if self.len == 0:
            return Empty()

        t = self.current.type

        # Order of precedence, hi -> lo
        unary_op = (MINUS, NOT)
        binary_op = (PLUS, MINUS, STAR, SLASH)

        # Literal or variable expression
        if self.len == 1:
            if t == IDENTIFIER:
                return Variable(self.current)

            return Literal(self.current)
        
        # Argument list expression. Expressions seperated by comma
        arg_toks = []
        while toks := self.seek(COMMA):
            arg_toks.append(toks)

        if len(arg_toks) > 0:
            arg_toks.append(self.rest)
            args = [self.proc(t, self.expr) for t in arg_toks]
            return Args(args)
        
        # Group expression. Check eof after group because it resets idx on failure
        if (inner := self.group(LEFT_PAREN, RIGHT_PAREN)) and self.eof:
            return Group(self.proc(inner, self.expr))
        
        # Binary expression, checked in order of precedence
        for sym in binary_op:
            # Remove prefixed symbols in case of unary expression
            while not self.eof and self.current.type in unary_op:
                self.next()

            left, right = self.split(sym)
            if not left or not right:
                continue

            # Extend left side to actual length if shortened above
            left_len = self.len - len(right) - 1
            left = self.tokens[:left_len]

            l, r = self.proc(left, self.expr), self.proc(right, self.expr)
            return Binary(l, r, self.at(len(left)))
        
        # Unary expression. Binary already parsed so remaining
        # tokens cannot be split by an operator.
        if self.first.type in unary_op:
            return Unary(self.proc(self.tokens[1:], self.expr), self.first)

        # Call expression. Last 'part' of expression has to be a group
        if self.last.type == RIGHT_PAREN:
            # Loop until at last group (arguments)
            while not self.eof:
                grp = self.group(LEFT_PAREN, RIGHT_PAREN)
                if not self.eof:
                    self.next()
                    continue

                # Get callee expression
                left = self.tokens[:self.len-len(grp)-2]
                callee = self.proc(left, self.expr)
                inner  = self.proc(grp, self.expr)
                return Call(callee, inner)

        self.err(f"invalid expression")

    # Parse and consume type name (with prefixed colon)
    def type(self) -> Type:
        self.expect(COLON, "':' before type")
        typ = self.expect(IDENTIFIER, "type")
        if typ.lexeme in typeword_lookup:
            return Type(typeword_lookup[typ.lexeme])

        self.err(f"undefined type {typ.lexeme}", True, typ)

    # ----------------------- STACK ----------------------- 

    # The parser uses a stack to control which tokens are currently being parsed.
    # This architecture allows generic helper methods to be used for any expression
    # or statement. It also handles iteration and nesting in the background.

    def add(self, tokens: list[Token]):
        self.list.append(tokens)
        self.idxs.append(0)
        self.ptr += 1

    def pop(self):
        self.list.pop()
        self.idxs.pop()
        self.ptr -= 1

    def next(self):
        self.idx += 1

    def prev(self):
        self.idx -= 1

    def at(self, idx: int) -> Token:
        return self.tokens[idx]

    @property
    def current(self) -> Token:
        return self.tokens[self.idx]

    @property
    def idx(self) -> int:
        return self.idxs[self.ptr]

    @idx.setter
    def idx(self, idx: int):
        self.idxs[self.ptr] = idx

    @property
    def len(self) -> int:
        return len(self.tokens)

    @property
    def tokens(self) -> list[Token]:
        return self.list[self.ptr]

    @property
    def rest(self) -> list[Token]:
        return self.tokens[self.idx:]

    @property
    def first(self) -> Token:
        return self.tokens[0]

    @property
    def last(self) -> Token:
        return self.tokens[self.len-1]

    @property
    def eof(self) -> bool:
        return self.idx >= self.len

    # ---------------------- HELPERS ----------------------

    # Add error to stack, terminates parsing if fatal
    def err(self, msg: str, fatal: bool = False, point: Token = None):
        first, last = self.first.col, self.last.col + len(self.last.lexeme)
        string, line = self.first.string, self.line

        # Specify token to highlight as err. Set error msg to tokens line
        if point != None:
            first, last = point.col, point.col+len(point.lexeme)
            string, line = point.string, point.line

        error = util.Error(msg, line, first, last, string, fatal)
        self.errstack.add(error)

    # Highlights specified token range in error
    def range_err(self, msg: str, tokens: list[Token], fatal: bool = False):
        self.proc(tokens, lambda: self.err(msg, fatal))

    # Expects and consumes single token. Return token
    def expect(self, tok: int, name: str) -> Token:
        if self.current.type != tok:
            self.err(f"expected {name}", True, self.current)
        t = self.current
        self.next()
        return t

    # Returns the tokens between curIdx and end_t. Empty list
    # on failure (falsy). Consumes end token.
    def seek(self, end_t: int) -> list[Token]:
        pairs = {
            LEFT_PAREN: RIGHT_PAREN,
            LEFT_SQUARE: RIGHT_SQUARE,
            LEFT_BRACE: RIGHT_BRACE
        }

        syms = {
            LEFT_PAREN: "(",
            LEFT_SQUARE: "[",
            LEFT_BRACE: "{",
            RIGHT_PAREN: ")",
            RIGHT_SQUARE: "]",
            RIGHT_BRACE: "}"
        }

        # Loops until EOF. If a token is a pair starter
        # it is appended to the closers stack. The closing
        # token must be found before end_t can be matched.
        interval = []
        closers = []
        opening = None
        start_idx = self.idx
        while self.idx < self.len:
            t = self.current.type

            if len(closers) == 0 and t == end_t:
                self.next()
                return interval

            # If a closing bracket is found before an opening
            if len(closers) == 0:
                for _, v in pairs.items():
                    if t == v:
                        closers.append(t)
                if len(closers) > 0:
                    break

            if t in pairs:
                # Todo: better tracking of which token was faulty
                opening = self.current
                closers.append(pairs[t])

            if len(closers) > 0 and t == closers[len(closers)-1]:
                closers.pop()
            
            interval.append(self.current)
            self.next()

        # Raise error if opening and closing brackets did
        # not match. Fallthrough is only if end_t was not found
        if len(closers) != 0:
            tok = opening
            if not self.eof: tok = self.current
            self.err("unmatched brackets", True, tok)

        self.idx = start_idx
        return []

    # Any of the given tokens are valid
    def any(self, *args):
        pass

    # Consumes token if present
    def optional(self, tok: int):
        pass
    
    # Returns token interval between left and right tokens.
    # Empty list on failure (falsy). Consumes tokens if valid
    def group(self, left: int, right: int) -> list[Token]:
        start_idx = self.idx
        if self.current.type != left:
            return []

        self.next()
        interval = self.seek(right)
        if not self.eof:
            self.idx = start_idx

        return interval

    # Returns token intervals of left and right of tok.
    # Two empty lists on failure (falsy). Consumes to eof
    def split(self, tok: int) -> tuple[list, list]:
        return self.seek(tok), self.rest

    # Same as split, but can have multiple split points
    def split_many(self, tok: int):
        pass

    # Expression starts with tok
    def prefix(self, tok: int):
        pass

    # Expression ends with tok
    def suffix(self, tok: int):
        pass

