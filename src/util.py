from tokens import NEWLINE

import os
if os.name == "nt":
    os.system("color")

def err(msg: str):
    print(f"ERROR: {msg}")
    exit(1)

class Error:
    def __init__(self, msg: str, line: int, start: int, end: int, string: str, fatal: bool = False):
        self.msg = msg
        self.line = line
        self.start = start
        self.end = end
        self.fatal = fatal
        self.string = string

    def red(self, text: str) -> str:
        return f"\033[91m{text}\033[0m"

    def print(self):
        print(f"{self.red('error:')} {self.msg}, line {self.line}")
        s = self.string
        s = s.replace("\n", "")
        s = s.replace("\t", 4*" ")
        print(f" {self.line} | {s}")
        diff = self.end-self.start
        if diff == 0:
            diff = 1
        print(f" {len(str(self.line))*' '} | " + self.red(" "*self.start + "^"*(diff)))
        print()

class ErrorStack:
    def __init__(self):
        self.errors = []

    def print(self):
        for e in self.errors:
            e.print()
        if len(self.errors) > 0:
            exit(1)

    def add(self, err: Error):
        self.errors.append(err)
        if err.fatal:
            self.print()

    def pop(self):
        self.errors.pop()

def print_tokens(tokens: list):
    for t in tokens:
        if t.type == NEWLINE: print("\\n", end=" ")
        else: print(t.lexeme, end=" ")
    print()
