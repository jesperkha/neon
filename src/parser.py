from tokens import *
from ast import *
import util

class Parser:
    def __init__(self, tokens: list[Token]):
        self.ast = AstNode(tokens)
        self.errstack = util.ErrorStack()

        # Current token list that is being parsed. Expressions usually
        # have recursive calls so a token list stack gives depth without
        # recursion and creating multiple objects.
        self.list = [tokens]
        # List of indecies from token stack
        self.idxs = [0]
        # Index of current token list (always last)
        self.ptr = 0

        self.line = 1

    # Parses token list. Returns AST. Exits on error
    def parse(self) -> AstNode:
        while self.idx < self.len:
            self.ast.stmts.append(self.stmt())

        self.errstack.print()
        return self.ast

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

        # Fallthrough is expression statement
        return ExprStmt(self.proc(self.seek(NEWLINE), self.expr))

    # Parses single expression
    def expr(self) -> Expr:
        if self.len == 0:
            return Empty()

        t = self.current.type

        unary_op = (MINUS, NOT)
        binary_op = (PLUS, MINUS, STAR, SLASH)

        # Literal or variable expression
        if self.len == 1:
            if t == IDENTIFIER:
                return Variable(self.current)

            return Literal(self.current)
        
        # Group expression. Check eof after group because it resets idx on failure
        if (inner := self.group(LEFT_PAREN, RIGHT_PAREN)) and self.eof:
            return Group(self.proc(inner, self.expr))
        
        # Binary expression, checked in order of precedence
        # Todo: binary should skip the first token when seeking op
        for sym in binary_op:
            left, right = self.split(sym)
            if not left or not right:
                continue

            l, r = self.proc(left, self.expr), self.proc(right, self.expr)
            return Binary(l, r, self.at(len(left)))
        
        # Unary expression. Binary already parsed so remaining
        # tokens cannot be split by an operator.
        if self.first.type in unary_op:
            return Unary(self.proc(self.tokens[1:], self.expr), self.first)

        self.err(f"invalid expression")

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
    def err(self, msg: str, fatal: bool = False, point: int = None):
        first, last = self.first.col, self.last.col + len(self.last.lexeme)
        if point != None: first, last = point, point+1
        error = util.Error(msg, self.line, first, last, self.first.string, fatal)
        self.errstack.add(error)

    # Expects and consumes single token
    def expect(self, tok: int):
        pass

    # Returns the tokens between curIdx and end_t. Empty list
    # on failure (falsy). Consumes end token. If last is True,
    # seek will get the tokens up to the last instance of end_t
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
        last_idx = self.idx
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
            self.err("unmatched brackets", True, tok.col)

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
        return self.seek(tok), self.tokens[self.idx:]

    # Same as split, but can have multiple split points
    def split_many(self, tok: int):
        pass

    # Expression starts with tok
    def prefix(self, tok: int):
        pass

    # Expression ends with tok
    def suffix(self, tok: int):
        pass

