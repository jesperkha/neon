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
    text = 'abc 123 1.0 "hello"'
    tokens = get_tokens(text)

    check = [
        Token(IDENTIFIER, "abc", 0, 0, "", KIND_NONE),
        Token(NUMBER, "123", 0, 0, "", KIND_NUMBER),
        Token(NUMBER, "1.0", 0, 0, "", KIND_NUMBER, True),
        Token(STRING, 'hello', 0, 0, "", KIND_STRING),
    ]

    test_attributes = ["type", "kind", "lexeme", "isfloat"]
    
    for i, t in enumerate(tokens):
        for attr in test_attributes:
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