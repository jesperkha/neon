import parser
import lexer
import tokens

def errorif(bin: bool, msg: str):
    if bin:
        print(msg)
        exit(1)

expr_cases = [
    # ["1 + 2", tokens.BINARY_EXPR],
    ["(a)", tokens.GROUP_EXPR],
    ["a", tokens.LITERAL_EXPR],
    ["[]", tokens.ARRAY_EXPR]
]

if __name__ == "__main__":
    for idx, c in enumerate(expr_cases):
        tks = lexer.tokenize(c[0])
        ast = parser.parse_expression(tks)
        errorif(ast.type != c[1], f"failed expr test case {idx+1}: expected '{c[1]}', got '{ast.type}'")
    
    print("test success")