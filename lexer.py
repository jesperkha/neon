import tokens

def err(msg: str) -> None:
    print(msg)
    exit(1)

class Token:
    def __init__(self, type: int, lexeme: str, line: int) -> None:
        self.lexeme = lexeme
        self.line   = line
        self.type   = type

def tokenize(source: str) -> list[Token]:
    "returns a list of `Token` with `type`, `lexeme`, and `line` properties. string lexemes include the quotes"

    token_list = []
    line = 1
    idx = -1
    
    while idx < len(source) - 1:
        idx += 1
        char = source[idx]
        nextchar = "" if idx >= len(source) - 1 else source[idx + 1]

        # newline
        if char == "\n":
            token_list.append(Token(tokens.NEWLINE, "NEWLINE", line))
            line += 1
            continue

        # ignored whitespace
        if char in tokens.whitespace_lookup:
            continue

        # strings
        if char == '"':
            string = '"'
            idx += 1 # skip starting quote
            terminated = False
            while idx < len(source):
                c = source[idx]
                if c != '"':
                    string += c
                else:
                    terminated = True
                    break
                idx += 1
            
            if not terminated:
                err(f"unterminated string, line {line}")

            string += '"'
            token_list.append(Token(tokens.STRING, string, line))
            continue

        # symbol
        if char in tokens.symbol_lookup:
            dbtoken = char + nextchar # double token
            if dbtoken in tokens.double_token_lookup:
                token_list.append(Token(tokens.double_token_lookup[dbtoken], dbtoken, line))
                idx += 1 # skip next token
            else:
                token_list.append(Token(tokens.symbol_lookup[char], char, line))
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
                    err(f"cannot start identifier with digit, line {line}")
                elif c == ".":
                    num += c
                    dot += 1
                else:
                    break
                idx += 1

            if dot > 1 or num.endswith("."):
                err(f"invalid number literal '{num}', line {line}")
            if num.replace(".", "").isdecimal():
                token_list.append(Token(tokens.NUMBER, num, line))

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
        
            if word in tokens.keyword_lookup: # check if reserved keyword first
                token_list.append(Token(tokens.keyword_lookup[word], word, line))
            else:
                token_list.append(Token(tokens.IDENTIFIER, word, line))
            idx -= 1
            continue
    
        # fallthrough is error
        err(f"unexpected token '{char}', line {line}")

    return token_list