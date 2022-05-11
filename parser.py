from tokens import *
from util import *

def parse(tokens: list) -> list[Statement]:
    return []

def parse_expression(tokens: list) -> Expression:
    if len(tokens) == 0:
        return Expression(EMPTY_EXPR, tokens, -1)

    first = tokens[0].type
    line  = tokens[0].line

    # a single token list can only be a literal value
    if len(tokens) == 1:
        if first in (STRING, NUMBER, IDENTIFIER):
            return Expression(LITERAL_EXPR, tokens, line)

        err(f"expected literal in expression, got '{tokens[0].lexeme}', line {line}")

    # group expression, cannot be empty (func calls are parsed elsewhere)
    if seek(tokens, LEFT_PAREN, RIGHT_PAREN) == len(tokens)-1:
        inner = parse_expression(tokens[1:len(tokens)-1])
        if inner.type == EMPTY_EXPR:
            err(f"expected expression in (), line {line}")

        group = Expression(GROUP_EXPR, tokens, line)
        group.value = inner
        return group

    # array literal, can be empty
    if seek(tokens, LEFT_SQUARE, RIGHT_SQUARE) == len(tokens)-1:
        inner = parse_expression(tokens[1:len(tokens)-1])
        array = Expression(ARRAY_EXPR, tokens, line)
        array.value = inner
        return array
    
    # Todo: diagnose expression issue
    print(tokens[0].type, seek(tokens, LEFT_PAREN, RIGHT_PAREN))
    err(f"invalid expression, line {line}")