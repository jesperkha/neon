from tokens import *
import ast
import util

from lexer import print_tokens # Debug

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

    # Parses token list. Returns AST. Exits on error
    def parse(self) -> ast.AstNode:
        tree = ast.AstNode()
        while self.idx < self.len:
            tree.stmts.append(self.stmt())

        self.errstack.print()
        return tree

    # Shorthand for invoking a procedure on a new stack frame
    def proc(self, tokens: list[Token], func) -> any:
        self.add(tokens)
        v = func()
        self.pop()
        return v

    # Parses single statement
    def stmt(self) -> ast.Stmt:
        self.line = self.current.line
        t = self.current.type

        # Note: define keyword statements before symbols

        # Return statement. Return outside func checked in scan.
        if t == RETURN:
            self.next()
            return ast.Return(self.proc(self.seek(NEWLINE), self.expr))

        # Function statement
        if t == FUNC:
            self.next()

            # Function name and left paren before params
            func_name = self.expect(IDENTIFIER, "function name")
            self.expect(LEFT_PAREN, "'('")

            # Consume all parameter names and types
            params = []
            while not self.eof and self.current.type != RIGHT_PAREN:
                name = self.expect(IDENTIFIER, "parameter name")
                params.append(ast.Param(name.lexeme, self.type()))
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
            return ast.Function(func_name.lexeme, params, return_t, block)
                
        # Block statement
        if t == LEFT_BRACE:
            return self.block()
        
        # Variable declaration
        if var := self.seek(COLON_EQUAL):
            if len(var) != 1 or var[0].type != IDENTIFIER:
                self.range_err("expected identifier on left side of ':='", var, True)

            expr = self.proc(self.seek(NEWLINE), self.expr)
            return ast.Declaration(var[0], expr)

        # Assignment. Left side is expression in case of
        # indexing or struct property, checked in scan.
        if var := self.seek(EQUAL):
            left = self.proc(var, self.expr)
            expr = self.proc(self.seek(NEWLINE), self.expr)
            return ast.Assignment(left, expr)

        # Fallthrough is expression statement
        return ast.ExprStmt(self.proc(self.seek(NEWLINE), self.expr))
    
    # Parses single block statement. Expects it, throws error if not found
    def block(self) -> ast.Block:
        self.expect(LEFT_BRACE, "block")
        self.expect(NEWLINE, "line break after brace")
        node = self.proc(self.seek(RIGHT_BRACE), self.parse)
        return ast.Block(node.stmts)

    # Parses single expression
    def expr(self) -> ast.Expr:
        if self.len == 0:
            return ast.Empty()

        t = self.current.type

        # Literal or variable expression
        if self.len == 1:
            if t == IDENTIFIER:
                return ast.Variable(self.current)

            return ast.Literal(self.current)
        
        # Argument list expression. Expressions seperated by comma
        arg_toks = []
        while toks := self.seek(COMMA):
            arg_toks.append(toks)

        if len(arg_toks) > 0:
            arg_toks.append(self.rest)
            args = [self.proc(t, self.expr) for t in arg_toks]
            return ast.Args(args)
        
        # Group expression. Check eof after group because it resets idx on failure
        if (inner := self.group(LEFT_PAREN, RIGHT_PAREN)) and self.eof:
            return ast.Group(self.proc(inner, self.expr))
        
        # Order of precedence, hight to low
        unary_ops = (MINUS, NOT)
        binary_ops = (PLUS, MINUS, STAR, SLASH)

        # Binary expression
        for op in binary_ops:
            # self.idx doesn't increment if no op symbol is found
            left, right = self.split_last(op)
            if not left or not right:
                continue

            # Magic to parse unary expressions
            if left[len(left)-1].type in binary_ops:
                continue

            l, r = self.proc(left, self.expr), self.proc(right, self.expr)
            return ast.Binary(l, r, self.at(len(left)))

        # Unary expression
        if self.first.type in unary_ops:
            return ast.Unary(self.proc(self.tokens[1:], self.expr), self.first)

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
                return ast.Call(callee, inner)

        self.err(f"invalid expression")

    # Parse and consume type name (with prefixed colon)
    def type(self) -> ast.Type:
        self.expect(COLON, "':' before type")
        typ = self.expect(IDENTIFIER, "type")
        if typ.lexeme in typeword_lookup:
            return ast.Type(typeword_lookup[typ.lexeme])

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
        while not self.eof:
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
                # Example??
                opening = self.current
                closers.append(pairs[t])

            if len(closers) > 0 and t == closers[len(closers)-1]:
                closers.pop()
            
            interval.append(self.current)
            self.next()
        
        # Exception for newline seek as eof might occur
        if end_t == NEWLINE and self.eof:
            return interval

        # Raise error if opening and closing brackets did
        # not match. Fallthrough is only if end_t was not found
        if len(closers) != 0:
            tok = opening
            if not self.eof: tok = self.current
            self.err("unmatched brackets", True, tok)

        self.idx = start_idx
        return []
    
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
    
    # Same as split but splits as the last instance of the token
    def split_last(self, tok: int) -> tuple[list, list]:
        tok_idx = 0
        while not self.eof:
            self.idx = tok_idx
            if not self.seek(tok):
                break
            tok_idx = self.idx
        
        if tok_idx == 0:
            return [], []

        return self.tokens[:tok_idx-1], self.tokens[tok_idx:]