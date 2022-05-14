import parser
import lexer
import tokens

def errorif(bin: bool, msg: str):
    if bin:
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
    # ["a[0]", tokens.EXPR_INDEX],
]

if __name__ == "__main__":
    failed = False
    for idx, c in enumerate(expr_cases):
        print(f"expr test {idx+1}: FAIL ", end="")
        try:
            tks = lexer.tokenize(c[0])
            ast = parser.parse_expression(tks)
            errorif(ast.type != c[1], f"(FAIL) expected '{c[1]}', got '{ast.type}'")
            print(f"\rexpr test {idx+1}: pass")
        except:
            failed = True
        
    if not failed:
        print("--- all tests passed ---")