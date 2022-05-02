import lexer
import parser

def main():
    with open("main.ce", "r+") as f:
        tokens = lexer.tokenize(f.read())
        stmts  = parser.parse(tokens)
        print(stmts)

if __name__ == "__main__":
    main()