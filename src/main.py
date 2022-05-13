import lexer
import parser
import util

def main():
    a = "(a + b) == c"
    tok = lexer.tokenize(a)
    expr = parser.parse_expression(tok)
    util.inspect_types(expr)

if __name__ == "__main__":
    main()
