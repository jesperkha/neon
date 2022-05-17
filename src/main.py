import lexer
import util
import parser
import os

# util.DEBUG_MODE = True

b = """

func main(): int {

    a := 0
    b: int = 1
    c = 0

    return a
}

"""

def main():
    a = "a := 0"
    ast = parser.parse(lexer.tokenize(b))
    for s in ast:
        util.inspect_stmt(s)

if __name__ == "__main__":
    os.system("color")
    main()
