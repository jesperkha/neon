import lexer
import util

def main():
    with open("main.ne") as f:
        source = f.read()
        tokens = lexer.Lexer(source).tokenize()

if __name__ == "__main__":
    main()
