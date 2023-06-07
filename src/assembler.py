from tokens import *

def assemble(files: list[str]) -> list[str]:
    return Assembler(files).assemble()

class Assembler:
    def __init__(self, files: list[str]) -> None:
        self.files = files

    def assemble(self):
        return "/"