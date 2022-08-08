import lexer
import matcher
import util

def main():
    with open("main.ne") as f:
        source = f.read()
        tokens = lexer.Lexer(source).tokenize()
        if util.err_count > 0:
            exit(1)

        res = matcher.Matcher(matcher.DTable(), tokens).match()
        print(res)

if __name__ == "__main__":
    main()
