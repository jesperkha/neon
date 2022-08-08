from tokens import *
import util

class Pattern:
    def __init__(self, *args):
        self.args = args

class AnyToken(Pattern):
    pass

class Any(Pattern):
    pass

class Optional(Pattern):
    pass

class Group:
    def __init__(self, left: int, pattern: Pattern, right: int):
        self.left = left
        self.right = right
        self.pattern = pattern

class Seek:
    def __init__(self, pattern: Pattern, stopper: int):
        self.pattern = pattern
        self.stopper = stopper


# Declaration table. Pattern declarations are stored in seperate object.
# The table is passed to a matcher along with a set of tokens.
class DeclarationTable:
    def __init__(self):
        self.register = {}
        self.default = ""
        
    def declare(self, name: str, pattern: Pattern):
        if not self.default:
            self.default = name
        self.register[name] = pattern

    def get(self, name: str) -> Pattern:
        return self.register[name]


class Matcher:
    def __init__(self, table: DeclarationTable, tokens: list[Token]):
        self.tokens = tokens
        self.table = table
        self.idx = 0

    # Matches the given tokens to the given declaration table.
    # Returns the result as a bool.
    def match(self) -> bool:
        m = self.match_pattern(self.table.default)
        if self.idx < len(self.tokens)-1:
            return False
        
        return m

    def match_tokens(self, tokens: list[Token]) -> bool:
        return Matcher(self.table, tokens).match()

    # Looks for the given token. Skips segments enclosed in
    # the token pairs listed below. Returns index of token or
    # -1 on failure.
    def seek(self, token: int|tuple, skip: bool = True) -> int:
        closed = {
            LEFT_PAREN: RIGHT_PAREN,
            LEFT_SQUARE: RIGHT_SQUARE
        }

        idx = self.idx
        stack = []
        while idx < len(self.tokens):
            t = self.tokens[idx].type
            if skip:
                if t in closed:
                    stack.append(closed[t])
                    idx += 1
                    continue
                
                if len(stack) > 0:
                    if t == stack[len(stack)-1]:
                        stack.pop()
                    idx += 1
                    continue

            if type(token) == tuple:
                if t in token:
                    return idx

            if t == token:
                return idx

            idx += 1

        return -1

    # Wrapper to reset the index after a failed match. Global
    # incrementation is done after a single success so if a
    # sub-pattern is true, but the parent pattern is false, the
    # index should be reset before matching the next pattern.
    def reset(func):
        def wrap(self, pattern: Pattern) -> bool:
            start_idx = self.idx
            m = func(self, pattern)
            if not m: self.idx = start_idx
            return m
        
        return wrap

    @reset
    def match_pattern(self, pattern: Pattern) -> bool:
        typ = type(pattern)
        
        # Match token type (int) to current token
        # Only iterate index if token was matched
        if typ == int:
            if self.tokens[self.idx].type == pattern:
                self.idx += 1
                return True

            return False

        # Match registered pattern by name (string)
        elif typ == str:
            return self.match_pattern(self.table.get(pattern))

        # Match any of the given token types (int)
        # Only iterate index if token was matched
        elif typ == AnyToken:
            if self.tokens[self.idx].type in pattern.args:
                self.idx += 1
                return True

            return False

        # Run matches for each of the optional patterns
        # to ensure that the index is iterated past the
        # optional pattern/token range.
        elif typ == Optional:
            start_idx = self.idx
            for p in pattern.args:
                self.idx = start_idx
                if self.match_pattern(p):
                    break

            return True

        # Match all sub-patterns in given Pattern
        # Index is automatically iterated by match_pattern()
        elif typ == Pattern:
            for p in pattern.args:
                if not self.match_pattern(p):
                    return False

            return True

        # Check to see if any pattern matches
        # Index is automatically iterated by match_pattern()
        elif typ == Any:
            for p in pattern.args:
                if self.match_pattern(p):
                    return True

            return False
        
        # Group pattern. Check for left token, seek right
        # token, and match the token interval between the two.
        elif typ == Group:
            left = self.tokens[self.idx]
            end_idx = self.seek(pattern.right, False)
            if left.type != pattern.left or end_idx == -1:
                return False

            m = self.match_tokens(self.tokens[self.idx+1:end_idx])
            self.idx = end_idx+1
            return m
        
        # Todo: implement Seek

        print(f"unknown pattern type: {typ}")
        exit()
