import util
import lexer
import parser
import scanner
import os
import sys

def compile():
    args = sys.argv[1:]
    if len(args) == 0:
        util.err("no input files")

    filename = args[0]
    if not filename.endswith(".ne"):
        util.err("input file must be a neon file (ending in '.ne')")
    if not os.path.isfile(filename):
        util.err(f"could not find '{filename}'")

    with open(filename, "r") as f:
        tok = lexer.tokenize(f.read())
        ast = parser.Parser(tok).parse()
        scn = scanner.Scanner().scan(ast)

if __name__ == "__main__":
    compile()
