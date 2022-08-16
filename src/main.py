import lexer
import util
import parser

def main():
    with open("main.ne") as f:
        source = f.read()
        tokens = lexer.Lexer(source).tokenize()
        ast    = parser.Parser(tokens).parse()
        print(ast)

if __name__ == "__main__":
    main()
