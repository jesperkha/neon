import lexer
import parser

def neon_build(filename: str) -> str:
    with open(filename) as f:
        source = f.read()
        tokens = lexer.get_tokens(source)
        tree   = parser.parse_tokens(tokens)
        tree.print()

if __name__ == "__main__":
    neon_build("test/main.ne")
