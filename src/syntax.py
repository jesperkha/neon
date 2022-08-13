from matcher import *

class NeonSyntaxTable(DeclarationTable):
    def __init__(self):
        super().__init__()
        self.declare("stmt", Seek("expr", NEWLINE), "invalid statement")
        self.declare("expr", Any("literal", "group", "unary", "binary"), "invalid expression")

        binary_op = AnyToken(PLUS, MINUS)
        unary_op  = AnyToken(NOT, MINUS)

        self.declare("literal", AnyToken(IDENTIFIER, STRING, CHAR, NUMBER, TRUE, FALSE))
        self.declare("group", Group(LEFT_PAREN, "expr", RIGHT_PAREN))
        self.declare("unary", Pattern(unary_op, "expr"))
        self.declare("binary", Split("expr", binary_op, "expr"))
