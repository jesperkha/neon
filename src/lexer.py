from tokens import *
from error import *

def print_tokens(tokens: list):
    for t in tokens:
        print(t.lexeme, end=" ")
        if t.type == NEWLINE:
            print()
    print()

@error_prone
def get_tokens(src: str) -> list[Token]:
    tokens = []
    start_idx = 0
    idx = 0
    start_col = 0
    col = 0
    line = 1
    line_string = ""

    # Read first line
    for c in src[idx:]:
        if c == '\n':
            break
        line_string += c
    
    while idx < len(src):

        # Comment
        if idx+1 < len(src) and (src[idx:idx+2] == "//"):
            while idx < len(src) and src[idx] != '\n':
                idx += 1
            continue

        # White space
        if src[idx] in whitespace_lookup:
            if src[idx] == '\n':
                tokens.append(Token(NEWLINE, "NEWLINE", line, col, line_string, KIND_NONE))

                # Read new line
                line_string = ""
                for c in src[idx+1:]:
                    if c == '\n':
                        break
                    line_string += c
                line += 1
                col = -1

            idx += 1
            col += 1
            continue

        # Identifier
        if src[idx].isalpha():
            start_idx = idx
            while idx < len(src) and (src[idx].isalnum() or src[idx] == '_'):
                idx += 1
            
            word = src[start_idx:idx]
            if word in keyword_lookup:
                tokens.append(Token(keyword_lookup[word], word, line, col, line_string, KIND_NONE))
            elif word in typeword_lookup:
                tokens.append(Token(IDENTIFIER, word, line, col, line_string, KIND_NONE))
            else:
                tokens.append(Token(IDENTIFIER, word, line, col, line_string, KIND_NONE))
            
            col += len(word)
            continue
        
        # Number
        if src[idx].isnumeric():
            start_idx = idx
            start_col = col
            dots = 0
            while idx < len(src) and (src[idx].isnumeric() or src[idx] == '.'):
                if src[idx] == '.':
                    dots += 1
                idx += 1
                col += 1
            
            if dots > 1:
                raise NeonSyntaxError("invalid number", line, start_col, col, line_string)

            number = src[start_idx:idx]
            tokens.append(Token(NUMBER, number, line, start_col, line_string, KIND_NUMBER, isfloat=dots>0))
            continue

        # Double symbol
        if idx + 1 < len(src):
            symbol = src[idx:idx+2]
            if symbol in double_symbol_lookup:
                tokens.append(Token(double_symbol_lookup[symbol], symbol, line, col, line_string, KIND_NONE))
                idx += 2
                col += 2
                continue

        # Single symbol
        if src[idx] in symbol_lookup:
            symbol = src[idx]
            tokens.append(Token(symbol_lookup[symbol], symbol, line, col, line_string, KIND_NONE))
            idx += 1
            col += 1
            continue

        # Strings
        if src[idx] == '"':
            string = ""
            start_col = col
            idx += 1
            col += 1
            while idx < len(src) and src[idx] != '"':
                if src[idx] == '\n':
                    raise NeonSyntaxError("unterminated string", line, start_col, col, line_string)

                string += src[idx]
                idx += 1
                col += 1
            
            if idx >= len(src):
                raise NeonSyntaxError("unterminated string", line, start_col, col, line_string)

            tokens.append(Token(STRING, string, line, start_col, line_string, KIND_STRING))
            idx += 1
            col += 1
            continue

        raise NeonSyntaxError("unknown token", line, col, col, line_string)

    return tokens