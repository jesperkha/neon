import lexer
import util
import parser
import os

# util.DEBUG_MODE = True

def main():
    a = "[a, b][f(x)] + -(c * !d + k)"
    tok = lexer.tokenize(a)
    expr = parser.parse_expression(tok)
    util.inspect_expr(expr)

if __name__ == "__main__":
    os.system("color")
    main()
