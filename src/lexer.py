# Lexer
# 
# This is neons lexer. It takes the raw text from a file and generates tokens from said
# input. Symbols, identifers, strings, numbers, and keywords are all each their own token 
# type. The lexer will also raise an error if it finds a symbol it does not recognise, if
# a string is malformed, or if a number is invalid.

from util import *
from tokens import *

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
            token_list.append(Token(NEWLINE, "NEWLINE", line))
            line += 1
            continue

        # ignored whitespace
        if char in whitespace_lookup:
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
            # Todo: add char type for ''
            token_list.append(Token(STRING, string, line))
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
                    continue

                token_list.append(Token(t, dbtoken, line))
                idx += 1 # skip next token
            else:
                token_list.append(Token(symbol_lookup[char], char, line))
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
                t = Token(NUMBER, num, line)
                t.isfloat = dot == 1
                token_list.append(t)

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
                token_list.append(Token(keyword_lookup[word], word, line))
            else:
                token_list.append(Token(IDENTIFIER, word, line))
            idx -= 1
            continue
    
        # fallthrough is error
        err(f"unexpected token '{char}', line {line}")

    return token_list