import lexer
import util
import parser
import os

# util.DEBUG_MODE = True

def main():
    a = "func main(): int {}"
    ast = parser.parse(lexer.tokenize(a))

if __name__ == "__main__":
    os.system("color")
    main()
