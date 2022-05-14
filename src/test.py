import parser
import lexer
import tokens
import os

def errorif(fail: bool, msg: str):
    if fail:
        print(msg)
        exit(1)

expr_cases = [
    ["1", tokens.EXPR_LITERAL],
    ["a", tokens.EXPR_VARIABLE],
    ["(a)", tokens.EXPR_GROUP],
    ["[]", tokens.EXPR_ARRAY],
    ["a + b", tokens.EXPR_BINARY],
    ["-a", tokens.EXPR_UNARY],
    ["a()", tokens.EXPR_CALL],
    ["a, b, c", tokens.EXPR_ARGS],
    ["a[0]", tokens.EXPR_INDEX],
]

if __name__ == "__main__":
    os.system("color")
    failed = False
    for idx, c in enumerate(expr_cases):
        print(f"expr test {idx+1}: \033[91mFAIL\033[0m ", end="")
        try:
            tks = lexer.tokenize(c[0])
            ast = parser.parse_expression(tks)
            errorif(ast.type != c[1], f"(FAIL) expected '{c[1]}', got '{ast.type}'")
            print(f"\rexpr test {idx+1}: \033[92mpass\033[0m")
        except:
            failed = True
        
    if not failed:
        print("--- all tests passed ---")