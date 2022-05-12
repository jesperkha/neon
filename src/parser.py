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
        if first in (STRING, NUMBER):
            return Expression(LITERAL_EXPR, tokens, line)
        elif first == IDENTIFIER:
            return Expression(VARIABLE_EXPR, tokens, line)

        err(f"expected literal in expression, got '{tokens[0].lexeme}', line {line}")

    # unrary expression, first token is unary operator
    if first in (MINUS, NOT) and (len(tokens) == 2 or tokens[1].type == LEFT_PAREN):
        unary = Expression(UNARY_EXPR, tokens, line)
        unary.right = parse_expression(tokens[1:])
        unary.operator = tokens[0]
        return unary

    # binary expression in order of precedence
    is_op = lambda typ: typ >= AND and typ <= SLASH
    operator, op_idx = None, 0
    for idx, t in enumerate(tokens):
        if not is_op(t.type):
            continue
        # if the tokens is lower precedence split earlier
        if not operator or (operator.type >= t.type and op_idx != idx - 1):
            operator = t
            op_idx = idx
    
    if operator:
        if op_idx == 0 or op_idx == len(tokens)-1:
            side = "left" if op_idx == 0 else "right"
            err(f"expected expression on {side} side of '{operator.lexeme}', line {line}")

        expr = Expression(BINARY_EXPR, tokens, line)
        expr.left  = parse_expression(tokens[:op_idx])
        expr.right = parse_expression(tokens[op_idx+1:])
        expr.operator = operator
        return expr

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

    # fallthrough means invalid expression
    err(f"invalid expression, line {line}")