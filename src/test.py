import parser
import lexer
import tokens
import os
import util
import scanner

# util.DEBUG_MODE = True

def errorif(fail: bool, msg: str):
    if fail:
        print(msg)
        exit(1)

expr_cases = [
    ["1", tokens.EXPR_LITERAL],
    ["a", tokens.EXPR_VARIABLE],
    ["(a)", tokens.EXPR_GROUP],
    ["[a, b]", tokens.EXPR_ARRAY],
    ["a + b", tokens.EXPR_BINARY],
    ["-a", tokens.EXPR_UNARY],
    ["a()", tokens.EXPR_CALL],
    ["a, b, c", tokens.EXPR_ARGS],
    ["a[0]", tokens.EXPR_INDEX],
]

stmt_cases = [
    ["a + b", tokens.STMT_EXPR],
    ["return a", tokens.STMT_RETURN],
    ["func main(): int {}", tokens.STMT_FUNC],
    ["a := 0", tokens.STMT_DECLARE],
    ["a: int = 0", tokens.STMT_DECLARE],
    ["a = 0", tokens.STMT_ASSIGN],
]

scan_cases_valid = [
    "a := 0",
    "a: int = 0",
    "a: float = 0.0",
    "a: bool = true",
    "1 + 1",
    "1.0 + 1.0",
    '"a" + "b"',
    "[1, 2.0]",
]

def test_cases(prefix: str, cases: list):
    for idx, c in enumerate(cases):
        print(f"{prefix} test {idx+1}: {util.text_red('FAIL')} ", end="")
        tks = lexer.tokenize(c[0])
        if prefix == "expr":
            ast = parser.parse_expression(tks)
        elif prefix == "stmt":
            stmts = parser.parse(tks)
            ast = stmts[0]
        errorif(ast.type != c[1], f"(FAIL) expected '{c[1]}', got '{ast.type}'")
        print(f"\r{prefix} test {idx+1}: {util.text_green('pass')}")


if __name__ == "__main__":
    os.system("color")
    test_cases("expr", expr_cases)
    test_cases("stmt", stmt_cases)
    i = 1
    for c in scan_cases_valid:
        print(f"scan test {i}: {util.text_red('FAIL')} ", end="")
        scanner.scan(parser.parse(lexer.tokenize(c)))
        print(f"\rscan test {i}: {util.text_green('pass')}")
        i += 1
    
    print("-----------------")
    print("all tests passed!")
    