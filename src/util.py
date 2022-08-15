def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"

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
        print(f" {self.line} | " + self.string.replace("\n", ""))
        print(f" {len(str(self.line))*' '} | " + red(" "*self.start + "^"*(self.end-self.start)))
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
        print(t.lexeme, end=" ")
    print()
