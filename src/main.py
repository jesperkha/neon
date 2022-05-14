import lexer
import util
import parser
import os

# util.DEBUG_MODE = True

def main():
    # a = input("> ")
    # a = "-6*2/( 2+1 * 2/3 +6) +8 * (8/4)"
    a = "a * -b"
    tok = lexer.tokenize(a)
    expr = parser.parse_expression(tok)
    util.inspect_expr(expr)

if __name__ == "__main__":
    os.system("color")
    main()
