import util
from lexer import get_tokens
from parser import parse_tokens
from tokens import *
import ast

cases = []

def test_func(func):
    cases.append(TestFunction(func))
    return None


class TestFunction:
    def __init__(self, func) -> None:
        self.func = func
        self.name = func.__name__
    
    def __call__(self):
        try:
            self.func()
            print(f"[ {util.green('pass')} ] {self.name}")
        except RuntimeError as err:
            print(f"[ {util.red('fail')} ] {self.name} {util.red(str(err))}")


@test_func
def TestTokenGeneration():
    text = 'abc 123 \n 1.0 "hello"'
    tokens = get_tokens(text)

    check = [
        Token(IDENTIFIER, "abc", 1, 0, text[:8], KIND_NONE),
        Token(NUMBER, "123", 1, 4, text[:8], KIND_NUMBER),
        Token(NEWLINE, "NEWLINE", 1, 8, text[:8], KIND_NONE),
        Token(NUMBER, "1.0", 2, 0, text[9:], KIND_NUMBER, True),
        Token(STRING, 'hello', 2, 4, text[9:], KIND_STRING),
    ]
    
    for i, t in enumerate(tokens):
        for attr in t.__dict__.keys():
            a = t.__getattribute__(attr)
            b = check[i].__getattribute__(attr)
            if a != b:
                raise RuntimeError(f"expected {attr} {b}, got {a}, input: {t.lexeme}")


@test_func
def TestExpressionParsing():
    # Todo: implement tree signature function
    cases = [
        "a + b",
        "(a + b) - c",
        "-a - -b",
        "foo(a, (b, c) + d)",
    ]

    for case in cases:
        tokens = get_tokens(case)
        tree = parse_tokens(tokens)


@test_func
def TestStatementParsing():
    pass

@test_func
def TestBlockParsing():
    pass
    

if __name__ == "__main__":
    for c in cases:
        c()