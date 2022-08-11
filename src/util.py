err_count = 0

class Error:
    def __init__(self, msg: str, line: int, start: int, end: int, string: str, fatal: bool = False):
        self.msg = msg
        self.line = line
        self.start = start
        self.end = end
        self.fatal = fatal
        self.string = string

    def print(self):
        print(f"{red('error:')} {self.msg}, line {self.line}")
        print(f" {self.line} | " + self.string.replace("\n", "\\"))
        print(f" {len(str(self.line))*' '} | " + red(" "*self.start + "^"*(self.end-self.start)))
        print()


def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"

def err(msg: str, line: str, start: int, end: int, fatal: bool = False):
    print("Compilation failed")
    print("| " + line.replace("\n", "\\"))
    print("| " + red(" "*start + "^"*(end-start)))
    print("> " + f"{red('error:')} {msg}")
    print()
    if fatal: exit(1)
    global err_count
    err_count += 1

def print_tokens(tokens: list):
    for t in tokens:
        print(t.lexeme, end=" ")
    print()
