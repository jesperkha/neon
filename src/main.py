import lexer
import util
import parser
import os

# util.DEBUG_MODE = True

b = """
func main(): int {

    return a
}
"""

def main():
    # a = "[]int"
    # parser.parse_type(lexer.tokenize(a))
    a = "func main(): int {}"
    ast = parser.parse(lexer.tokenize(b))
    for s in ast:
        util.inspect_stmt(s)

if __name__ == "__main__":
    os.system("color")
    main()
