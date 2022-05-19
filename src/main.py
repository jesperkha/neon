import util
import lexer
import parser
import os
import sys

# util.DEBUG_MODE = True

def compile():
    args = sys.argv[1:] # omit filename
    if len(args) == 0:
        util.err("no input files")

    filename = args[0]
    if not filename.endswith(".ne"):
        util.err("input file must be a neon file (ending in '.ne')")
    if not os.path.isfile(filename):
        util.err(f"could not find '{filename}'")

    with open(filename, "r") as f:
        ast = parser.parse(lexer.tokenize(f.read()))
        for s in ast:
            util.inspect_stmt(s)


def main():
    compile()

if __name__ == "__main__":
    os.system("color")
    main()
