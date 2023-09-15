from lexer import get_tokens
from parser import parse_tokens

from tokens import *
import util

cases = []

def test_func(func):
    cases.append(TestFunction(func))
    return func


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
    text = 'abc 123 \n1.0 "hello"'
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
    cases = [
        ("a + b", "EBVTVTT"),
        ("(a + b) - c", "EBGBVTVTTVTT"),
        ("-a - -b", "EBUVTTVUTTT"),
        ("foo(a, bar(b, c) + d)", "ECVTAVTBCVTAVTVTVTT"),
    ]

    for case in cases:
        tokens = get_tokens(case[0])
        tree = parse_tokens(tokens)
        sign = tree.stmts[0].signature.short()
        if sign != case[1]:
            raise RuntimeError(f"expected signature {case[1]}, got {sign}, input: {case[0]}")


@test_func
def TestStatementParsing():
    raise RuntimeError("not implemented")


if __name__ == "__main__":
    for c in cases:
        c()