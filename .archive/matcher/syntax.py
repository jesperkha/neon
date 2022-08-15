from matcher import *

class NeonSyntaxTable(DeclarationTable):
    def __init__(self):
        super().__init__()
        self.declare("program", List("stmt"))

        self.declare("stmt", Any("newline", "block"), "invalid statement")

        self.declare("newline", NEWLINE)
        self.declare("block", Pattern(LEFT_BRACE, Seek(List("stmt"), RIGHT_BRACE)))
        #self.declare("exprStmt", Seek("expr", NEWLINE))

        self.declare("expr", Any("literal", "group", "unary", "binary"), "invalid expression")

        binary_op = AnyToken(PLUS, MINUS)
        unary_op  = AnyToken(NOT, MINUS)

        self.declare("empty", Empty())
        self.declare("literal", AnyToken(IDENTIFIER, STRING, CHAR, NUMBER, TRUE, FALSE))
        self.declare("group", Group(LEFT_PAREN, "expr", RIGHT_PAREN))
        self.declare("unary", Pattern(unary_op, "expr"))
        self.declare("binary", Split("expr", binary_op, "expr"))
