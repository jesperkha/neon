from tokens import *
from util import *

def parse(tokens: list) -> list[Statement]:
    return []

def parse_expression(tokens: list) -> Expression:
    if len(tokens) == 0:
        return Expression(EXPR_EMPTY, tokens, -1)

    first = tokens[0].type
    line  = tokens[0].line

    # Todo: verify parens are correctly opened/closed

    # a single token list can only be a literal value
    if len(tokens) == 1:
        if first in (STRING, NUMBER):
            return Expression(EXPR_LITERAL, tokens, line)
        elif first == IDENTIFIER:
            expr = Expression(EXPR_VARIABLE, tokens, line)
            # Todo: check variable lookup for variable type
            expr.value.set(TYPE_VAR) # placeholder
            return expr

        err(f"expected literal in expression, got '{tokens[0].lexeme}', line {line}")

    # unrary expression, first token is unary operator
    if first in (MINUS, NOT) and (len(tokens) == 2 or tokens[1].type == LEFT_PAREN):
        unary = Expression(EXPR_UNARY, tokens, line)
        unary.right = parse_expression(tokens[1:])
        unary.operator = tokens[0]
        return unary

    # binary expression in order of precedence
    is_op = lambda typ: typ >= AND and typ <= SLASH
    operator, op_idx = None, 0
    for idx, t in enumerate(tokens):
        # Todo: skip over groups to avoid splitting inside them
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

        expr = Expression(EXPR_BINARY, tokens, line)
        expr.left  = parse_expression(tokens[:op_idx])
        expr.right = parse_expression(tokens[op_idx+1:])
        expr.operator = operator
        return expr

    # group expression, cannot be empty (func calls are parsed elsewhere)
    if seek(tokens, LEFT_PAREN, RIGHT_PAREN) == len(tokens)-1:
        inner = parse_expression(tokens[1:len(tokens)-1])
        if inner.type == EXPR_EMPTY:
            err(f"expected expression in (), line {line}")

        group = Expression(EXPR_GROUP, tokens, line)
        group.inner = inner
        return group

    # array literal, can be empty
    if seek(tokens, LEFT_SQUARE, RIGHT_SQUARE) == len(tokens)-1:
        inner = parse_expression(tokens[1:len(tokens)-1])
        array = Expression(EXPR_ARRAY, tokens, line)
        array.inner = inner
        return array

    # fallthrough means invalid expression
    err(f"invalid expression, line {line}")