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
        self.curlist = [tokens]

    # Parses token list. Returns AST. Exits on error
    def parse(self) -> AstNode:
        return self.ast

    # Parses single statement
    def stmt(self) -> Stmt:
        pass

    # Parses single expression
    def expr(self) -> Expr:
        pass

    # ----------------------- STACK ------------------------------

    # The parser uses a stack to control which tokens are currently being parsed.
    # This architecture allows generic helper methods to be used for any expression
    # or statement. It also handles iteration and nesting in the background.

    def add(self, tokens: list[Token]):
        pass

    def pop(self):
        pass

    def current(self) -> int:
        pass

    def next(self) -> int:
        pass

    def idx(self) -> int:
        pass

    # ---------------------- HELPERS -----------------------------

    # Expects and consumes single token
    def expect(self, tok: int):
        pass

    # Returns index of end token. Skips groups
    def seek(self, end: int):
        pass

    # Any of the given tokens are valid
    def any(self, args*):
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

