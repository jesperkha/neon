import os

import lexer
import parser

def main():
    with open("test/main.ne") as f:
        source = f.read()
        tokens = lexer.Lexer(source).tokenize()
        tree   = parser.Parser(tokens).parse()
        tree.print()

if __name__ == "__main__":
    main()
