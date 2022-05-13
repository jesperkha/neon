from tokens import *
from util import *

# Parses token list into list of statements
def parse(tokens: list) -> list[Statement]:
    return []

# Seeks and returns the index of the closing token of a given list.
def seek(tokens: list[Token], start_t: int, end_t: int, start_idx: int = 0) -> int:
    t = 0
    if tokens[0].type != start_t:
        return -1

    for idx, tok in enumerate(tokens[start_idx:]):
        if tok.type == start_t: t += 1
        elif tok.type == end_t: t -= 1
        if t == 0:
            return idx

    return -1

# Token iterator skips over group expressions
class TokenIter:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.idx = -1
    
    def __iter__(self):
        return self

    def __next__(self) -> tuple[int, Token]:
        self.idx += 1
        if self.idx >= len(self.tokens):
            raise StopIteration
        t = self.tokens[self.idx]
        if t.type == LEFT_PAREN:
            end_idx = seek(self.tokens, LEFT_PAREN, RIGHT_PAREN, self.idx)
            if end_idx == -1:
                raise StopIteration
            self.idx = end_idx + self.idx
            return self.__next__()

        return self.idx, self.tokens[self.idx]

# Returns true if the open and closing token types match
def verify_brackets(tokens: list[Token], start_t: int, end_t: int) -> bool:
    t = 0
    for tok in tokens:
        if tok.type == start_t: t += 1
        elif tok.type == end_t: t -= 1
    return t == 0

# Recursively parses token list into an expression tree
def parse_expression(tokens: list) -> Expression:
    if len(tokens) == 0:
        return Expression(EXPR_EMPTY, tokens, -1)

    first = tokens[0].type
    line  = tokens[0].line

    if not verify_brackets(tokens, LEFT_PAREN, RIGHT_PAREN):
        err(f"unmatched parentheses, line {line}")
    if not verify_brackets(tokens, LEFT_SQUARE, RIGHT_SQUARE):
        err(f"unmatched square brackets, line {line}")

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
    
    # Todo: checl for argument expression

    # unrary expression, first token is unary operator
    if first in (MINUS, NOT) and (len(tokens) == 2 or tokens[1].type == LEFT_PAREN):
        unary = Expression(EXPR_UNARY, tokens, line)
        unary.right = parse_expression(tokens[1:])
        unary.operator = tokens[0]
        return unary

    # binary expression in order of precedence
    is_op = lambda typ: typ >= AND and typ <= SLASH
    operator, op_idx = None, 0
    for idx, t in TokenIter(tokens):
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

    # check for function call expression
    if first == IDENTIFIER:
        second = tokens[1].type
        if second == LEFT_PAREN:
            callee = tokens[0]
            inner = parse_expression(tokens[2:len(tokens)-1])
            call = Expression(EXPR_CALL, tokens, line)
            call.inner = inner
            call.callee = callee
            return call

        elif second == LEFT_SQUARE:
            # Todo: implement array index expr
            err("array index expr not implemented yet")

    # fallthrough means invalid expression
    err(f"invalid expression, line {line}")