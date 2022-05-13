import lexer
import parser
import util

def main():
    # a = input("> ")
    a = "f()"
    tok = lexer.tokenize(a)
    expr = parser.parse_expression(tok)
    util.inspect_expr(expr)

if __name__ == "__main__":
    main()
