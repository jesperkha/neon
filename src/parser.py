from tokens import *
from util import *

# Seeks and returns the index of the closing token of a given list, -1 on fail
def seek(tokens: list[Token], start_t: int, end_t: int, start_idx: int = 0) -> int:
    t = 0
    if tokens[start_idx].type != start_t:
        return -1

    idx = start_idx
    while idx < len(tokens):
        tok = tokens[idx]
        if tok.type == start_t: t += 1
        elif tok.type == end_t: t -= 1
        if t == 0:
            return idx
        idx += 1

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
    def __init__(self, tokens):
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
    return stmt_parser(tokens).parse()

# Statement parser object to keep state when doing recursive parsing
# Also makes it easier to do expect_x() parsing
class stmt_parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.idx = 0
        self.line = 0
        self.statements = []
    
    def parse(self) -> list[Statement]:
        while self.idx < len(self.tokens):
            stmt = self.parse_stmt()
            self.statements.append(stmt)
        return self.statements
    
    def parse_stmt(self) -> Statement:
        tok = self.advance()
        typ = tok.type

        if typ == RETURN:
            stmt = Statement(STMT_RETURN, self.line)
            stmt.expr = self.expect_expr()
            return stmt
        elif typ == FUNC:
            stmt = Statement(STMT_FUNC, self.line)
            stmt.name  = self.expect_identifier()
            stmt.expr  = self.expect_args()
            stmt.vtype = self.expect_type()
            stmt.block = self.expect_block()
            interupt("func")
            return stmt

        # fallthrough means expression statement
        self.back() # go back one
        stmt = Statement(STMT_EXPR, self.line)
        stmt.expr = self.expect_expr()
        return stmt
    
    # Peeks next token, raises error on EOF
    def peek(self) -> Token:
        if self.idx + 1 >= len(self.tokens):
            err(f"unexpected end of input, line {self.line}")
        return self.tokens[self.idx+1]
    
    # Returns current token. Does not consume it
    def current(self) -> Token:
        return self.tokens[self.idx]
    
    # Consumes and returns the current Token. Raises error on EOF
    def advance(self, e: bool = False) -> Token:
        if self.idx >= len(self.tokens):
            if e: err(f"unexpected end of input, line {self.line}")
            return None

        cur = self.tokens[self.idx]
        self.line = cur.line # better error handling
        self.idx += 1
        return cur
    
    # Goes back one token and returns it. NO CHECK FOR OUT OF RANGE
    def back(self) -> Token:
        self.idx -= 1
        return self.tokens[self.idx]
    
    # Looks at current token to check for the keyword (token type). If the
    # keyword is not found an error is raised. Consumes token
    def expect_keyword(self, keyword: int):
        kw = self.advance(True)
        if kw.type != keyword:
            kw_name = [k for k, v in keyword_lookup.items() if v == keyword][0]
            err(f"expected keyword '{kw_name}', found '{kw.lexeme}', line {self.line}")
    
    # Seeks a NEWLINE token and parses the expression in interval.
    # Returns expression. Raises error on EOF. Consumes NEWLINE token
    def expect_expr(self) -> Expression:
        start_i, n = self.idx, 0
        while t := self.advance():
            if t.type == NEWLINE:
                n = 1
                break
        token_range = self.tokens[start_i:self.idx-n]
        return parse_expression(token_range)
    
    # Checks if next token is identifier. Raises error. Consumes token
    def expect_identifier(self) -> Token:
        t = self.advance(True)
        if t.type != IDENTIFIER:
            err(f"expected identifier, got '{t.lexeme}', line {self.line}")
        return t
    
    # Checks to see if the next tokens indicate an argument list. Raises
    # error on fail. Consumes tokens. RETURNED EXPR CAN BE NON-ARGS TOO
    def expect_args(self) -> Expression:
        t = self.current()
        if t.type != LEFT_PAREN:
            err(f"expected arg list, line {self.line}")
        end_idx = seek(self.tokens, LEFT_PAREN, RIGHT_PAREN, self.idx)
        if end_idx == -1:
            err(f"expected right paren after arg list, line {self.line}")
        interval = self.tokens[self.idx+1:end_idx]
        self.idx = end_idx + 1
        return parse_expression(interval)

    # Checks for type declaration (including colon). Raises error
    # on invalid type tokens. Consumes type
    def expect_type(self) -> Type:
        if self.advance(True).type != COLON:
            print()
            err(f"expected colon brefore type, line {self.line}")
        stack = []
        while t := self.advance(True):
            if t.type == IDENTIFIER:
                stack.append(t.lexeme)
                break
            elif t.type == STAR:
                stack.append("*")
            elif t.type == LEFT_SQUARE:
                self.advance(True) # skip next bracket
                stack.append("[]")
            else:
                err(f"invalid token in type: '{t.lexeme}', line {self.line}")
        return Type() # Todo: create type object
    
    # Checks for block statement. Consumes block and returns block
    # Raises error on no block, as well as internal statement parsing
    def expect_block(self) -> Statement:
        if self.current().type != LEFT_BRACE:
            err(f"expected block, line {self.line}")
        err("block not implemented yet")

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
            return Expression(EXPR_VARIABLE, tokens, line)

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
    # Todo: re-implement but with check for type prefix
    # if seek(tokens, LEFT_SQUARE, RIGHT_SQUARE) == len(tokens)-1:
    #     debug("array", tokens)
    #     inner = parse_expression(tokens[1:len(tokens)-1])
    #     array = Expression(EXPR_ARRAY, tokens, line)
    #     array.inner = inner
    #     return array

    # function call expression, ends with '(args)'
    last = tokens[len(tokens)-1].type
    if last == RIGHT_PAREN:
        debug("call", tokens)
        begin_idx = seek_back(tokens, LEFT_PAREN, RIGHT_PAREN)
        if begin_idx == 0:
            err(f"expected function expression before args, line {line}")

        call = Expression(EXPR_CALL, tokens, line)
        call.inner = parse_expression(tokens[begin_idx+1:len(tokens)-1])
        call.callee = parse_expression(tokens[:begin_idx])
        return call

    # array index expression, ends with '[index]'
    elif last == RIGHT_SQUARE:
        debug("index", tokens)
        begin_idx = seek_back(tokens, LEFT_SQUARE, RIGHT_SQUARE)
        if begin_idx == 0:
            err(f"expected expression before index, line {line}")

        inner = parse_expression(tokens[begin_idx+1:len(tokens)-1])
        if inner.type == EXPR_EMPTY:
            err(f"missing expression as index, line {line}")

        index = Expression(EXPR_INDEX, tokens, line)
        index.array = parse_expression(tokens[:begin_idx])
        index.inner = inner
        return index

    # fallthrough means invalid expression
    debug("fallthrough", tokens)
    err(f"invalid expression, line {line}")