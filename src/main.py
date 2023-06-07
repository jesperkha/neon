import lexer
import parser
import scanner
import builder
import assembler

def neon_build(filename: str) -> str:
    with open(filename) as f:
        source = f.read()
        tokens = lexer.get_tokens(source)
        tree   = parser.parse_tokens(tokens)
        scanner.scan_tree(tree)

        output = builder.build([tree])
        print(output)
        
        files  = assembler.assemble(output)
        print(files)

if __name__ == "__main__":
    neon_build("test/main.ne")
