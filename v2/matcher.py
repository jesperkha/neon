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

class Matcher:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.register = {}
        self.idx = 0

        self.new("literal", AnyToken(IDENTIFIER, STRING, CHAR, NUMBER))
        self.new("binary", Pattern("expr", "expr", sep=Seperator(PLUS, MINUS)))
        self.new("expr", Any("literal", "binary"))

        m = self.matches("expr")
        print(m)

    def new(self, name: str, pattern: Pattern):
        self.register[name] = pattern

    def matches(self, pattern: Pattern) -> bool:
        typ = type(pattern)

        # Special case:
        # If the pattern has a seperator, the token list will
        # be split the given token types in the seperator tuple.
        # Each chunk of the split will be matched against the
        # respective pattern.
        if typ == Pattern and pattern.seperator:
            idx = self.idx
            split = []
            while idx < len(self.tokens):
                t = self.tokens[idx]
                if t.type in pattern.seperator.types:
                    split.append(idx)
                    if not pattern.seperator.multiple:
                        break

                idx += 1

            # If one or more seperator tokens were found, match chunks.
            # Else continue with the rest of the match cases below
            if len(split) > 0:
                # Todo: split token list and match each chunk
                print("-------------")
                exit()
                pass
        
        # Match token type (int) to current token
        # Only iterate index if token was matched
        if typ == int:
            m = self.tokens[self.idx].type == pattern
            if m: self.idx += 1
            return m

        # Match registered pattern by name (string)
        elif typ == str:
            print(pattern)
            return self.matches(self.register[pattern])

        # Match any of the given token types (int)
        # Only iterate index if token was matched
        elif typ == AnyToken:
            m = self.tokens[self.idx].type in pattern.args
            if m: self.idx += 1
            return m

        # Run matches for each of the optional patterns
        # to ensure that the index is iterated past the
        # optional pattern/token range.
        elif typ == Optional:
            for p in pattern.args:
                self.matches(p)
            return True

        # Match all sub-patterns in given Pattern
        # Index is automatically iterated by matches()
        elif typ == Pattern:
            if pattern.sep:
                pass
            
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

        print(f"unknown pattern type: {typ}")
        exit()
