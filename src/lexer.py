from tokens import *
import util

def print_tokens(tokens: list[Token]):
    for t in tokens:
        print(t.lexeme if t.lexeme else "//", end=" ")

class Lexer:
    def __init__(self, source: str):
        self.tokens = []
        self.source = source
        self.line = 1
        self.col  = -1
        self.idx  = -1
        self.string = ""

        self.errstack = util.ErrorStack()

    def tokenize(self) -> list[Token]:
        while self.idx < len(self.source) - 1:
            char = self.next()
            self.string += char
            nextchar = "" if self.idx >= len(self.source) - 1 \
                          else self.source[self.idx+1]
            
            if char == "\n":
                self.add(NEWLINE, "", self.line, self.col)
                self.line += 1
                self.string = ""
                self.col = -1
                continue
            
            if char == "\t":
                self.col += 3
                self.string += ""
                continue

            # Non-newline whitespace is ignored
            if char in whitespace_lookup:
                continue

            # Parse string and char literals
            string_chars = ("'", '"')
            if char in string_chars:
                start_char = char
                start_col = self.col
                string, not_terminated = self.word(lambda c: c != start_char)

                if not_terminated:
                    self.err(f"unterminated string", start_col, self.col+1)
                    continue

                self.string += self.next()
                string = f"{start_char}{string}{start_char}"

                # Char
                if start_char == "'":
                    if len(string) != 3:
                        self.err(f"char type must be one character long", start_col, self.col+1)
                        continue

                    self.add(CHAR, string, self.line, start_col)
                    continue
                
                # String
                self.add(STRING, string, self.line, start_col)
                continue

            # Single and double symbol tokens
            if char in symbol_lookup:
                double = char + nextchar

                # Double token
                if double in double_token_lookup:
                    typ = double_token_lookup[double]
                    
                    # Skip to end of line for comments
                    if typ == COMMENT:
                        self.skip_line()
                        self.shift()
                        continue

                    self.add(typ, double, self.string, self.col)
                    self.string += nextchar
                    self.next()

                # Single token
                else:
                    self.add(symbol_lookup[char], char, self.line, self.col)

                continue

            # Number literals
            if char.isdecimal():
                start_col = self.col
                number, _ = self.word(lambda c: c.isdecimal() or c == ".")
                number = char + number
                dots = number.count(".")

                if dots > 1 or number.endswith(".") or number.startswith("."):
                    self.err(f"invalid number literal", start_col, self.col)
                    continue

                if not number.replace(".", "").isdecimal():
                    self.err(f"cannot start variable name with number", start_col, self.col)
                    continue

                isfloat = dots == 1
                self.add(NUMBER, number, self.line, start_col, isfloat)
                continue
            
            if char == "." and nextchar.isdecimal():
                self.err(f"number literal cannot start with a '.'", self.col, self.col+1)
                continue

            # Keywords and identifiers
            ident_symbols_start = ("_", "$")
            ident_symbols = ("_")

            if char.isalnum() or char in ident_symbols_start:
                start_col = self.col
                word, _ = self.word(lambda c: c.isalnum() or c.isdecimal() or c in ident_symbols)
                word = char + word

                if word in keyword_lookup:
                    self.add(keyword_lookup[word], word, self.line, start_col)
                else:
                    self.add(IDENTIFIER, word, self.line, start_col)
                continue

            # Fatal: invalid character
            self.err(f"unexpected token '{char}'", self.col, self.col+1)

        self.errstack.print()
        return self.tokens

    # Seeks a character that does not satisfy the given end function (returns false).
    # Returns (word, eof)
    def word(self, end) -> tuple[str, bool]:
        word = ""
        while self.idx < len(self.source) - 1:
            char = self.next()
            if char == "\n":
                self.prev()
                return word, True

            if not end(char):
                self.prev()
                return word, False

            word += char
            self.string += char
        
        return "", True

    # Adds a token to the list
    def add(self, typ: int, lexeme: str, line: int, col: int, isfloat: int = False):
        n = (self.idx, self.string, self.col)
        self.word(lambda _: True)
        self.tokens.append(Token(typ, lexeme, line, col, self.string, isfloat))
        self.idx, self.string, self.col = n

    # Go forward one character, returns character
    def next(self) -> str:
        self.idx += 1
        self.col += 1
        if self.idx < len(self.source):
            return self.source[self.idx]

        return ""

    # Go back one character
    def prev(self):
        self.idx -= 1
        self.col -= 1

    # Skips rest of tokens and seeks newline
    def skip_line(self):
        while self.idx < len(self.source) - 1:
            if self.source[self.idx] == "\n":
                self.prev()
                return
            self.next()

    # Remove first character of string
    def shift(self):
        self.string = self.string[1:]

    # Add rest of line to self.string before printing error
    def err(self, msg: str, start_col: int, end_col: int, fatal: bool = False):
        self.word(lambda _: True)
        self.errstack.add(util.Error(msg, self.line, start_col, end_col, self.string, fatal))
        self.skip_line()

