import lexer
import matcher
import util
import syntax

def main():
    with open("main.ne") as f:
        source = f.read()
        tokens = lexer.Lexer(source).tokenize()
        if util.err_count > 0:
            exit(1)

        matched = matcher.Matcher(syntax.NeonSyntaxTable(), tokens).match()
        print(f"\nResult: {matched}")

if __name__ == "__main__":
    main()
