from tokens import *
import util

class Empty:
    pass

class Pattern:
    def __init__(self, *args):
        self.args = args

class AnyToken(Pattern):
    pass

class Any(Pattern):
    pass

class AnyConsume(Pattern):
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

class Split:
    def __init__(self, left: Pattern, sep: int, right: Pattern):
        self.left = left
        self.right = right
        self.seperator = sep

class SplitMany:
    def __init__(self, pattern: Pattern, sep: int):
        self.pattern = pattern
        self.seperator = sep

# Declaration table. Pattern declarations are stored in seperate object.
# The table is passed to a matcher along with a set of tokens.
class DeclarationTable:
    def __init__(self):
        self.register = {}
        self.errmsgs = {}
        self.default = ""
        
    def declare(self, name: str, pattern: Pattern, err: str = None):
        if not self.default:
            self.default = name
        self.register[name] = pattern
        self.errmsgs[name] = err if err else f"expected {name}"

    def get(self, name: str) -> Pattern:
        return self.register[name]

    def err(self, pattern: str) -> str:
        return self.errmsgs[pattern]

class Matcher:
    def __init__(self, table: DeclarationTable, tokens: list[Token], indent: int = 0):
        self.tokens = tokens
        self.idx = 0
        self.indent = indent
        self.ispattern = False

        self.table = table
        self.default = self.table.default

        self.errstack = util.ErrorStack()

    # Matches the given tokens to the given declaration table.
    # Returns the result as a bool.
    def match(self, pattern: Pattern = None) -> bool:
        if len(self.tokens) == 0:
            return type(pattern) == Empty

        if pattern:
            self.default = pattern

        # If the pattern doesnt match, or the token list was not fully consumed
        if not self.match_pattern(self.default) or self.idx != len(self.tokens):
            first, last = self.tokens[0], self.tokens[len(self.tokens)-1]
            start, end = first.column, last.column+len(last.lexeme)
            self.errstack.add(util.Error(self.table.err(self.default), first.line, start, end, first.string, True))
            return False

        return True

    def match_tokens(self, tokens: list[Token], pattern: Pattern, consume_all: bool = False) -> bool:
        return Matcher(self.table, tokens, self.indent).match(pattern)

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
                
                elif len(stack) > 0:
                    if t == stack[len(stack)-1]:
                        stack.pop()

            if len(stack) == 0:
                if type(token) == AnyToken:
                    if t in token.args:
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

            # Print debug info
            tab = self.indent * "  "
            pat_name = type(pattern).__name__ if type(pattern) not in (str, int) else f'"{pattern}"'
            print(f"{tab}Trying {pat_name}: ", end="")
            util.print_tokens(self.tokens[start_idx:])
            self.indent += 1
            m = func(self, pattern)
            self.indent -= 1

            if not m or (not self.ispattern and self.idx != len(self.tokens)):
                print(f"{tab}Failed: {pat_name}")
                self.idx = start_idx
                return False

            print(f"{tab}Success: {pat_name}")
            return m
        
        return wrap

    @reset
    def match_pattern(self, pattern: Pattern) -> bool:
        typ = type(pattern)
        
        # Match token type (int) to current token
        # Always iterate index (is reset if match fails)
        if typ == int:
            self.idx += 1
            return self.tokens[self.idx-1].type == pattern

        # Match registered pattern by name (string)
        elif typ == str:
            return self.match_pattern(self.table.get(pattern))

        # Match any of the given token types (int)
        # Always iterate index (is reset if match fails)
        elif typ == AnyToken:
            self.idx += 1
            return self.tokens[self.idx-1].type in pattern.args

        # Run matches for each of the optional patterns
        # to ensure that the index is iterated past the
        # optional pattern/token range.
        elif typ == Optional:
            for p in pattern.args:
                if self.match_pattern(p):
                    break

            return True

        # Match all sub-patterns in given Pattern
        # Index is automatically iterated by match_pattern()
        elif typ == Pattern:
            self.ispattern = True
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

        # Same as Any but the pattern must consume all remaining
        # tokens to be valid.
        elif typ == AnyConsume:
            start_idx = self.idx
            for p in pattern.args:
                if self.match_pattern(p):
                    if self.idx == len(self.tokens):
                        return True
                
                self.idx = start_idx

            return False
        
        # Group pattern. Check for left token, seek right
        # token, and match the token interval between the two.
        elif typ == Group:
            left = self.tokens[self.idx]
            # Todo: add optional Group and Seek arg for non-skip
            end_idx = self.seek(pattern.right)
            if left.type != pattern.left or end_idx == -1:
                return False

            m = self.match_tokens(self.tokens[self.idx+1:end_idx], pattern.pattern)
            self.idx = end_idx+1
            return m
        
        # Seeks stopper token and matches the prefix interval
        elif typ == Seek:
            end_idx = self.seek(pattern.stopper, False)
            if end_idx == -1:
                return False

            m = self.match_tokens(self.tokens[self.idx:end_idx], pattern.pattern)
            self.idx = end_idx+1
            return m

        # Split token list at seperator token and match both sides
        elif typ == Split:
            split_idx = self.seek(pattern.seperator)
            if split_idx == -1:
                return False
            
            left = self.tokens[self.idx:split_idx]
            right = self.tokens[split_idx+1:]
            if len(left) == 0 or len(right) == 0:
                return False
            
            l = self.match_tokens(left, pattern.left)
            r = self.match_tokens(right, pattern.right)
            self.idx = len(self.tokens)
            return l and r

        # Todo: implement SplitMany
        elif typ == SplitMany:
            pass

        print(f"unknown pattern type: {typ}")
        exit()
