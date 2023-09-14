import util

class NeonError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class NeonSyntaxError(NeonError):
    def __init__(self, msg: str, line: int, start: int, end: int, string: str, fatal: bool = False):
        self.msg = msg
        self.line = line
        self.start = start
        self.end = end
        self.string = string
        self.fatal = fatal

    def __str__(self) -> str:
        s = f"{util.red('error:')} {self.msg}, line {self.line}\n"
        s += f" {self.line} | " + self.string.replace("\n", "").replace("\t", 4*" ") + "\n"
        diff = self.end-self.start if self.end != self.start else 1
        s += f" {len(str(self.line))*' '} | " + util.red(" "*self.start + "^"*diff) + "\n"
        return s


def error_prone(func):
    def wrap(*args):
        try:
            return func(*args)
        except NeonSyntaxError as err:
            print(err)
            exit(1)

    return wrap