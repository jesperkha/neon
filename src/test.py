from lexer import Lexer
from parser import Parser

def main():
    with open("test/cases.ne") as f:
        txt = f.read()
        cases = txt.split("---")
        test_nr = 1
        
        for test in cases:
            try:
                print(f"Case {test_nr}: ", end="")
                tokens = Lexer(test).tokenize()
                tree   = Parser(tokens).parse()
                print("success")
            except:
                print("fail")
            test_nr += 1

if __name__ == "__main__":
    main()