from tokens import *
import util

class Lexer:
    def __init__(self, source: str):
        self.tokens = []
        self.source = source
        self.line = 1
        self.col  = -1
        self.idx  = -1

        self.string = ""

    def tokenize(self) -> list[Token]:
        while self.idx < len(self.source) - 1:
            char = self.next()
            self.string += char
            nextchar = "" if self.idx >= len(self.source) - 1 else self.source[self.idx + 1]

            if char == "\n":
                self.add(NEWLINE, "NEWLINE", self.line, self.col)
                self.line += 1
                self.string = ""
                self.col = -1
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
                    self.err(f"unterminated string, line {self.line}", start_col, self.col+1)
                    continue

                self.string += self.next()
                string = f"{start_char}{string}{start_char}"

                # Char
                if start_char == "'":
                    if len(string) != 3:
                        self.err(f"char type must be one character long, line {self.line}", start_col, self.col)
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
                    self.err(f"invalid number literal, line {self.line}", start_col, self.col)
                    continue

                if not number.replace(".", "").isdecimal():
                    self.err(f"cannot start variable name with number, line {self.line}", start_col, self.col)
                    continue

                isfloat = dots == 1
                self.add(NUMBER, number, self.line, start_col, isfloat)
                continue
            
            if char == "." and nextchar.isdecimal():
                self.err(f"number literal cannot start with a '.', line {self.line}", self.col, self.col+1)
                continue

            # Keywords and identifiers
            if char.isalnum() or char in ("_", "$"):
                start_col = self.col
                word, _ = self.word(lambda c: c.isalnum() or c.isdecimal() or c == "_")
                word = char + word

                if word in keyword_lookup:
                    self.add(keyword_lookup[word], word, self.line, start_col)
                else:
                    self.add(IDENTIFIER, word, self.line, start_col)
                continue

            # Fatal: invalid character
            self.err(f"unexpected token {char}, line {self.line}", self.col, self.col+1)

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
        self.tokens.append(Token(typ, lexeme, line, col, isfloat))

    def next(self) -> str:
        self.idx += 1
        self.col += 1
        if self.idx < len(self.source):
            return self.source[self.idx]

        return ""

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
        self.word(lambda _: False)
        util.err(msg, self.string, start_col, end_col, fatal)
        self.skip_line()
            
# Returns list of Token from source text
def tokenize(source: str) -> list[Token]:
    "returns a list of `Token` with `type`, `lexeme`, and `line` properties. string lexemes include the quotes"
    token_list = []
    line = 1
    idx = -1
    col = -1
    string_line = ""
    
    while idx < len(source) - 1:
        idx += 1
        col += 1
        char = source[idx]
        nextchar = "" if idx >= len(source) - 1 else source[idx + 1]

        string_line += char

        # newline
        if char == "\n":
            #token_list.append(Token(NEWLINE, "NEWLINE", line))
            col = -1
            line += 1
            string = ""
            continue

        # ignored whitespace
        if char in whitespace_lookup:
            continue

        # strings
        string_c = ("'", '"')
        if char in string_c:
            string  = char
            start_c = char
            idx += 1 # skip starting quote
            terminated = False

            start_col = col

            while idx < len(source):
                c = source[idx]
                if c != start_c:
                    string += c
                else:
                    terminated = True
                    break
                idx += 1
                col += 1
                string_line += c
            
            if not terminated:
                util.err(f"unterminated string, line {line}", string_line, start_col, col)

            # char type
            string += start_c
            if start_c == "'":
                if len(string) != 3: # including ' '
                    util.err(f"char type must be one character long, line {line}")
                #token_list.append(Token(CHAR, string, line))
                continue

            # string type
            #token_list.append(Token(STRING, string, line))
            continue

        # symbol
        if char in symbol_lookup:
            dbtoken = char + nextchar # double token
            if dbtoken in double_token_lookup:
                t = double_token_lookup[dbtoken]
                
                # skip to end of line for comments
                if t == COMMENT:
                    while idx < len(source):
                        if source[idx] == "\n":
                            break
                        idx += 1
                    line += 1
                    continue

                #token_list.append(Token(t, dbtoken, line))
                idx += 1 # skip next token
                string_line += nextchar
                col += 1
            else:
                #token_list.append(Token(symbol_lookup[char], char, line))
                pass
            continue

        # number
        if char.isdecimal():
            num = ""
            dot = 0
            while idx < len(source):
                c = source[idx]
                if c.isdecimal():
                    num += c
                elif c.isidentifier(): # check invalid identifiers to avoid error handling later
                    util.err(f"cannot start identifier with digit, line {line}")
                elif c == ".":
                    num += c
                    dot += 1
                else:
                    break
                idx += 1

            if dot > 1 or num.endswith("."):
                util.err(f"invalid number literal '{num}', line {line}")
            if num.replace(".", "").isdecimal():
                t = Token(NUMBER, num, line)
                t.isfloat = dot == 1
                string_line += t.lexeme[1:]
                col += len(t.lexeme) -1 
                #token_list.append(t)

            idx -= 1
            continue

        # identifier
        if char.isalnum() or char == "_":
            word = ""
            while idx < len(source):
                c = source[idx]
                if c.isalnum() or c.isdecimal() or c == "_":
                    word += c
                else:
                    break
                idx += 1
        
            if word in keyword_lookup: # check if reserved keyword first
                #token_list.append(Token(keyword_lookup[word], word, line))
                pass
            else:
                #token_list.append(Token(IDENTIFIER, word, line))
                pass
            idx -= 1
            string_line += word[1:]
            col += len(word) - 1
            continue
    
        # fallthrough is error
        util.err(f"unexpected token '{char}', line {line}")

    return token_list
