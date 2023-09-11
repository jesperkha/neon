from lexer import get_tokens
from tokens import *

cases = []

def test_func(func):
    cases.append(TestFunction(func))
    return None


class TestFunction:
    def __init__(self, func) -> None:
        self.func = func
        self.name = func.__name__
    
    def __call__(self):
        print(f"{self.name} ", end="")
        try:
            self.func()
            print("pass")
        except RuntimeError as err:
            print(f"failed")
            print(err)


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
    

if __name__ == "__main__":
    for c in cases:
        c()