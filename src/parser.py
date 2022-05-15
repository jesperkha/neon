from tokens import *
from util import *

# Seeks newline token starting at cur_idx, returns NEWLINE index, -1 on fail
def seek_newline(tokens: list[Token], cur_idx: int) -> int:
    for i in range(cur_idx, len(tokens)):
        if tokens[i].type == NEWLINE:
            return i
    return len(tokens)

# Seeks and returns the index of the closing token of a given list, -1 on fail
def seek(tokens: list[Token], start_t: int, end_t: int) -> int:
    t = 0
    if tokens[0].type != start_t:
        return -1

    for idx, tok in enumerate(tokens):
        if tok.type == start_t: t += 1
        elif tok.type == end_t: t -= 1
        if t == 0:
            return idx

    return -1

# Same as seek() but starts from end of list. Handles swap of start_t and end_t
def seek_back(tokens: list[Token], start_t: int, end_t: int) -> int:
    t = 0
    last_idx = len(tokens) - 1
    if tokens[last_idx].type != end_t:
        return -1
    
    for idx in range(last_idx, 0, -1):
        tok = tokens[idx]
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
    
    def check_bracket(self, start_t: int, end_t: int) -> tuple[int, Token]:
        if self.tokens[self.idx].type == start_t:
            end_idx = seek(self.tokens[self.idx:], start_t, end_t)
            if end_idx == -1:
                raise StopIteration
            self.idx = end_idx + self.idx
            return self.__next__()
        return None

    def __next__(self) -> tuple[int, Token]:
        self.idx += 1
        if self.idx >= len(self.tokens):
            raise StopIteration
        if n := self.check_bracket(LEFT_PAREN, RIGHT_PAREN): return n
        if n := self.check_bracket(LEFT_SQUARE, RIGHT_SQUARE): return n
        return self.idx, self.tokens[self.idx]

# Returns true if the open and closing token types match
def verify_brackets(tokens: list[Token], start_t: int, end_t: int) -> bool:
    t = 0
    for tok in tokens:
        if tok.type == start_t: t += 1
        elif tok.type == end_t: t -= 1
    return t == 0

# Parses token list into list of statements
def parse(tokens: list) -> list[Statement]:
    statements, idx = [], 0
    while idx < len(tokens):
        stmt, offset = parse_statement(tokens[idx:])
        statements.append(stmt)
        idx += offset

    return statements

# Parses the statement and returns said statement along with the new
# index offset which is added to idx in parse()
def parse_statement(tokens: list[Token]) -> tuple[Statement, int]:
    first = tokens[0].type
    line  = tokens[0].line

    if first == RETURN:
        # given RETURN
        # expect expression
        err("return not implemented")
    # elif first == FUNC:
    #   given 'func'
    #   expect identifier
    #   expect GROUP[ARGS]
    #   expect :
    #   expect type
    #   expect block

    # fallthrough means expression statement
    end_idx = seek_newline(tokens, 0)
    expr = parse_expression(tokens[:end_idx])
    return Statement(STMT_EXPR, expr, line), end_idx



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
        debug(f"single token", tokens)
        if first in (STRING, NUMBER):
            return Expression(EXPR_LITERAL, tokens, line)
        elif first == IDENTIFIER:
            expr = Expression(EXPR_VARIABLE, tokens, line)
            expr.value.set(TYPE_VAR) # sets type from lookup when doing ast pass
            return expr

        err(f"expected literal in expression, got '{tokens[0].lexeme}', line {line}")

    # argument expression (comma separated values). check if token list contains any
    # commas since any expression with commas on top level must be an argument expression
    arg_split = []
    last_idx = -1
    for idx, t in TokenIter(tokens):
        if t.type == COMMA:
            arg_split.append(tokens[last_idx+1:idx])
            last_idx = idx

    if len(arg_split) != 0:
        debug("arg list", tokens)
        arg_split.append(tokens[last_idx+1:])
        args = Expression(EXPR_ARGS, tokens, line)
        args.exprs = [parse_expression(e) for e in arg_split]
        return args

    # expression operators in order of precedence
    is_op = lambda typ: typ >= AND and typ <= NOT
    operator, op_idx, num_ops = None, 0, 0
    for idx, t in TokenIter(tokens):
        if not is_op(t.type):
            continue

        num_ops += 1
        # 1. the operator is not yet set so set it now
        # 2. the found operator is lower or equal precedence and is not the token after
        # 3. even if the first op is the lowest it cannot be a pos 0 since that would
        #    be a unary and since unary only has one operator this will never be
        #    triggered for such an expression
        if not operator or (operator.type >= t.type and op_idx != idx - 1) or op_idx == 0:
            operator = t
            op_idx = idx
    
    if operator:
        # unary expression. first token must be the operator and only one operator
        # can be present. it must also be a valid unary operator. error is handled
        # when parsing binary
        if op_idx == 0 and num_ops == 1 and first in (MINUS, NOT):
            debug("unary", tokens)
            unary = Expression(EXPR_UNARY, tokens, line)
            unary.right = parse_expression(tokens[1:])
            unary.operator = tokens[0]
            return unary

        # if its not a unary its binary. first check if the first or last token is
        # an operator since that would be an invalid expression
        debug("binary", tokens)
        if op_idx == 0 or op_idx == len(tokens)-1:
            side = "left" if op_idx == 0 else "right"
            err(f"expected expression on {side} side of '{operator.lexeme}', line {line}")

        expr = Expression(EXPR_BINARY, tokens, line)
        expr.left  = parse_expression(tokens[:op_idx])
        expr.right = parse_expression(tokens[op_idx+1:])
        expr.operator = operator
        return expr

    # group expression. a group cannot be empty. if the remaining tokens do not
    # form a complete group thers either a syntax error or not a group expression
    if seek(tokens, LEFT_PAREN, RIGHT_PAREN) == len(tokens)-1:
        debug("group", tokens)
        inner = parse_expression(tokens[1:len(tokens)-1])
        if inner.type == EXPR_EMPTY:
            err(f"expected expression in (), line {line}")

        group = Expression(EXPR_GROUP, tokens, line)
        group.inner = inner
        return group

    # array literal, can be empty
    if seek(tokens, LEFT_SQUARE, RIGHT_SQUARE) == len(tokens)-1:
        debug("array", tokens)
        inner = parse_expression(tokens[1:len(tokens)-1])
        array = Expression(EXPR_ARRAY, tokens, line)
        array.inner = inner
        return array

    # function call expression, ends with '(args)'
    last = tokens[len(tokens)-1].type
    if last == RIGHT_PAREN:
        debug("call", tokens)
        callee = tokens[0]
        inner = parse_expression(tokens[2:len(tokens)-1])
        call = Expression(EXPR_CALL, tokens, line)
        call.inner = inner
        call.callee = callee
        return call

    # array index expression, ends with '[index]'
    elif last == RIGHT_SQUARE:
        debug("index", tokens)
        begin_idx = seek_back(tokens, LEFT_SQUARE, RIGHT_SQUARE)
        inner = parse_expression(tokens[begin_idx+1:len(tokens)-1])
        if inner.type == EXPR_EMPTY:
            err(f"missing expression as index, line {line}")

        index = Expression(EXPR_INDEX, tokens, line)
        index.inner = inner
        index.array = parse_expression(tokens[:begin_idx])
        return index

    # fallthrough means invalid expression
    debug("fallthrough", tokens)
    err(f"invalid expression, line {line}")