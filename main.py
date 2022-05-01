import lexer

def main():
    with open("src.ce", "r+") as f:
        s = f.read()
        tokens = lexer.tokenize(s)
        for t in tokens:
            print(t.lexeme)

if __name__ == "__main__":
    main()