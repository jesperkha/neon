import parser
import lexer
import tokens
import os
import util

# util.DEBUG_MODE = True

def errorif(fail: bool, msg: str):
    if fail:
        print(msg)
        exit(1)

expr_cases = [
    # ["1", tokens.EXPR_LITERAL],
    # ["a", tokens.EXPR_VARIABLE],
    # ["(a)", tokens.EXPR_GROUP],
    # ["[]", tokens.EXPR_ARRAY],
    # ["a + b", tokens.EXPR_BINARY],
    # ["-a", tokens.EXPR_UNARY],
    # ["a()", tokens.EXPR_CALL],
    # ["a, b, c", tokens.EXPR_ARGS],
    # ["a[0]", tokens.EXPR_INDEX],
]

stmt_cases = [
    ["a + b", tokens.STMT_EXPR],
    ["return a", tokens.STMT_RETURN],
]

def test_cases(prefix: str, cases: list):
    passed = True
    for idx, c in enumerate(cases):
        print(f"{prefix} test {idx+1}: \033[91mFAIL\033[0m ", end="")
        try:
            tks = lexer.tokenize(c[0])
            if prefix == "expr":
                ast = parser.parse_expression(tks)
            elif prefix == "stmt":
                stmts = parser.parse(tks)
                ast = stmts[0]
            errorif(ast.type != c[1], f"(FAIL) expected '{c[1]}', got '{ast.type}'")
            print(f"\r{prefix} test {idx+1}: \033[92mpass\033[0m")
        except:
            passed = False
    return passed


if __name__ == "__main__":
    os.system("color")
    if test_cases("expr", expr_cases) and test_cases("stmt", stmt_cases):
        print("-----------------")
        print("all tests passed!")