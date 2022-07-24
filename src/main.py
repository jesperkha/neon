import util
import os
import sys
import shutil
import pathlib

from lexer import tokenize
from parser import Parser
from scanner import Scanner
from compiler import Compiler

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
        tok = tokenize(f.read())
        ast = Parser(tok).parse()
        ast = Scanner().scan(ast)
        src = Compiler().compile(ast)

        with open("main.c", "w") as c:
            c.write(src)

        path = f"{pathlib.Path(__file__).parent.parent.absolute()}/lib"
        os.system(f"gcc -I{path} -o main *.c {path}/stdneon.c")
        os.system("./main")

if __name__ == "__main__":
    compile()
