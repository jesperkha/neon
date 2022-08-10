from matcher import *

class NeonSyntaxTable(DeclarationTable):
    def __init__(self):
        super().__init__()
        self.declare("stmt", Seek("expr", NEWLINE))
        self.declare("expr", All("literal", "group", "unary", "binary"))

        self.declare("literal", AnyToken(IDENTIFIER, STRING, CHAR, NUMBER, TRUE, FALSE))
        self.declare("group", Group(LEFT_PAREN, "expr", RIGHT_PAREN))
        self.declare("unary", Pattern(AnyToken(NOT, MINUS), "expr"))
        self.declare("binary", Split("expr", PLUS, "expr"))

