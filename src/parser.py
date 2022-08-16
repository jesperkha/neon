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

    # Parses token list. Returns AST. Exits on error
    def parse(self) -> AstNode:
        while self.idx() < self.len():
            self.stmt()

        return self.ast

    # Parses single statement
    def stmt(self) -> Stmt:
        self.expr()

    # Parses single expression
    def expr(self) -> Expr:
        util.print_tokens(self.tokens()[self.idx():]) # Debug
        self.next()

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

    def current(self) -> Token:
        return self.tokens()[self.idx()]

    def next(self):
        self.idxs[self.ptr] += 1

    def set(self, idx: int):
        self.idxs[self.ptr] = idx

    def idx(self) -> int:
        return self.idxs[self.ptr]

    def len(self) -> int:
        return len(self.tokens())

    def tokens(self) -> list[Token]:
        return self.list[self.ptr]

    # ---------------------- HELPERS ----------------------

    # Expects and consumes single token
    def expect(self, tok: int):
        pass

    # Returns index of end token. Skips groups
    def seek(self, end: int):
        pass

    # Any of the given tokens are valid
    def any(self, *args):
        pass

    # Consumes token if present
    def optional(self, tok: int):
        pass
    
    # Parses expression between left and right tokens
    def group(self, left: int, right: int):
        pass

    # Parses expressions on left and right of tok
    def split(self, tok: int):
        pass

    # Same as split, but can have multiple split points
    def split_many(self, tok: int):
        pass

    # Expression starts with tok
    def prefix(self, tok: int):
        pass

    # Expression ends with tok
    def suffix(self, tok: int):
        pass

