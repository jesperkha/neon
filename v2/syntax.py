from matcher import *

class NeonSyntaxTable(DeclarationTable):
    def __init__(self):
        super().__init__()
        self.declare("stmt", Seek("expr", NEWLINE))
        self.declare("expr", Any("literal", "group"))
        self.declare("literal", AnyToken(IDENTIFIER, STRING, CHAR, NUMBER, TRUE, FALSE))
        self.declare("group", Group(LEFT_PAREN, "expr", RIGHT_PAREN))
