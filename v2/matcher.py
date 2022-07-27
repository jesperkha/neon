from tokens import *
import util

class Seperator:
    def __init__(self, *types: int, multiple: bool = False):
        self.types = types
        self.multiple = multiple

class Pattern:
    def __init__(self, *args, sep: Seperator = None):
        self.args = args
        self.seperator = sep

class AnyToken(Pattern):
    pass

class Any(Pattern):
    pass

class Optional(Pattern):
    pass

class Group:
    def __init__(self, left: int, pattern: Pattern, right: int):
        self.left = left
        self.pattern = pattern
        self.right = right

class Matcher:
    def __init__(self, tokens: list[Token]):
        self.register = {}
        self.tokens = tokens
        self.idx = 0

        self.new("group", Group(LEFT_PAREN, "expr", RIGHT_PAREN))
        self.new("literal", AnyToken(IDENTIFIER, STRING))

        self.new("expr", Any("literal", "group")) 

        self.default_pattern = "expr"

        m = self.match_all()
        print(m)

    def new(self, name: str, pattern: Pattern):
        self.register[name] = pattern

    def match_all(self) -> bool:
        m = self.matches(self.default_pattern)
        if self.idx < len(self.tokens)-1:
            return False
        
        return m

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
    def matches(self, pattern: Pattern) -> bool:
        typ = type(pattern)
        
        # If the pattern has a seperator, the token list will
        # be split the given token types in the seperator tuple.
        # Each chunk of the split will be matched against the
        # respective pattern.
        if typ == Pattern and pattern.seperator:
            # Todo: redo to support multiple seperators
            split_idx = self.seek(pattern.seperator.types)

            # A seperator is required if specified, return
            # false if none is found.
            if split_idx == -1:
                return False

            split = (
                self.tokens[self.idx:split_idx],
                self.tokens[split_idx+1:len(self.tokens)]
            )

            # Todo: add recursive check for seperator
            print("Seperator not implemented")
            exit()
        
        # Match token type (int) to current token
        # Only iterate index if token was matched
        elif typ == int:
            if self.tokens[self.idx].type == pattern:
                self.idx += 1
                return True

            return False

        # Match registered pattern by name (string)
        elif typ == str:
            return self.matches(self.register[pattern])

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
                if self.matches(p):
                    break

            return True

        # Match all sub-patterns in given Pattern
        # Index is automatically iterated by matches()
        elif typ == Pattern:
            for p in pattern.args:
                if not self.matches(p):
                    return False

            return True

        # Check to see if any pattern matches
        # Index is automatically iterated by matches()
        elif typ == Any:
            for p in pattern.args:
                if self.matches(p):
                    return True

            return False
        
        elif typ == Group:
            left = self.tokens[self.idx]
            end_idx = self.seek(pattern.right, False)
            if left.type != pattern.left or end_idx == -1:
                return False

            # Todo: add recursive check for token interval
            print("group match")
            exit()

        print(f"unknown pattern type: {typ}")
        exit()
