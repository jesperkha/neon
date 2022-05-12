import parser
import lexer
import tokens

def errorif(bin: bool, msg: str):
    if bin:
        print(msg)
        exit(1)

expr_cases = [
    ["a", tokens.LITERAL_EXPR],
    ["(a)", tokens.GROUP_EXPR],
    ["[]", tokens.ARRAY_EXPR],
    ["a + b", tokens.BINARY_EXPR],
    ["-a", tokens.UNARY_EXPR]
]

if __name__ == "__main__":
    for idx, c in enumerate(expr_cases):
        print(f"expr test {idx+1}: ", end="")
        tks = lexer.tokenize(c[0])
        ast = parser.parse_expression(tks)
        errorif(ast.type != c[1], f"(FAIL) expected '{c[1]}', got '{ast.type}'")
        print("pass")
    
    print("--- all tests passed ---")