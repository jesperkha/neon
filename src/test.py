import parser
import lexer
import tokens

def errorif(bin: bool, msg: str):
    if bin:
        print(msg)
        exit(1)

expr_cases = [
    ["1", tokens.LITERAL_EXPR],
    ["a", tokens.VARIABLE_EXPR],
    ["(a)", tokens.GROUP_EXPR],
    ["[]", tokens.ARRAY_EXPR],
    ["a + b", tokens.BINARY_EXPR],
    ["-a", tokens.UNARY_EXPR],
    # Todo: add call parsing
    # ["a()", tokens.CALL_EXPR],
    # Todo: add array indexing parsing
    # ["a[0]", tokens.INDEX_EXPR],
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