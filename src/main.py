import os

import lexer
import parser

def main():
    os.system("color")

    with open("main.ne") as f:
        source = f.read()
        tokens = lexer.Lexer(source).tokenize()
        lexer.print_tokens(tokens)
        ast    = parser.Parser(tokens).parse()
        ast.print()

if __name__ == "__main__":
    main()
