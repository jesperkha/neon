from tokens import *
import util

def print_tokens(tokens: list):
    for t in tokens:
        print(t.lexeme, end=" ")
        if t.type == NEWLINE:
            print()
    print()

def get_tokens_new(src: str) -> list[Token]:
    tokens = []
    start_pos = 0
    pos = 0
    line = 1
    line_string = ""

    # Read first line
    for c in src[pos:]:
        if c == '\n':
            break
        line_string += c
    
    while pos < len(src):

        # Comment
        if pos+1 < len(src) and (src[pos:pos+2] == "//"):
            while pos < len(src) and src[pos] != '\n':
                pos += 1
            continue

        # White space
        if src[pos] in whitespace_lookup:
            if src[pos] == '\n':
                tokens.append(Token(NEWLINE, "NEWLINE", line, pos, line_string, KIND_NONE))

                # Read new line
                line_string = ""
                for c in src[pos+1:]:
                    if c == '\n':
                        break
                    line_string += c
                line += 1

            pos += 1
            continue

        # Identifier
        if src[pos].isalpha():
            start_pos = pos
            while pos < len(src) and (src[pos].isalnum() or src[pos] == '_'):
                pos += 1
            
            word = src[start_pos:pos]
            if word in keyword_lookup:
                tokens.append(Token(keyword_lookup[word], word, line, start_pos, line_string, KIND_NONE))
            elif word in typeword_lookup:
                tokens.append(Token(IDENTIFIER, word, line, start_pos, line_string, KIND_NONE))
            else:
                tokens.append(Token(IDENTIFIER, word, line, start_pos, line_string, KIND_NONE))
            continue
        
        # Number
        if src[pos].isnumeric():
            start_pos = pos
            dots = 0
            while pos < len(src) and (src[pos].isnumeric() or src[pos] == '.'):
                if src[pos] == '.':
                    dots += 1
                pos += 1
            
            if dots > 1:
                util.Error("invalid number", line, start_pos, pos, line_string).print()
                exit(1)

            number = src[start_pos:pos]
            tokens.append(Token(NUMBER, number, line, start_pos, line_string, KIND_NUMBER, isfloat=dots>0))
            continue

        # Double symbol
        if pos + 1 < len(src):
            symbol = src[pos:pos+2]
            if symbol in double_symbol_lookup:
                start_pos = pos
                pos += 2
                tokens.append(Token(double_symbol_lookup[symbol], symbol, line, start_pos, line_string, KIND_NONE))
                continue

        # Single symbol
        if src[pos] in symbol_lookup:
            start_pos = pos
            symbol = src[pos]
            pos += 1
            tokens.append(Token(symbol_lookup[symbol], symbol, line, start_pos, line_string, KIND_NONE))
            continue

        # Strings
        if src[pos] == '"':
            start_pos = pos
            string = ""
            pos += 1
            while pos < len(src) and src[pos] != '"':
                if src[pos] == '\n':
                    util.Error("unterminated string", line, start_pos, pos, line_string).print()
                    exit(1)

                string += src[pos]
                pos += 1
            
            if pos >= len(src):
                util.Error("unterminated string", line, start_pos, pos, line_string).print()
                exit(1)

            pos += 1
            tokens.append(Token(STRING, string, line, start_pos, line_string, KIND_STRING))
            continue

        start_pos = pos
        util.syntax_error("unknown token", line, start_pos, pos, line_string)
        exit(1)

    return tokens