from tokens import *

def err(msg: str) -> None:
    print(msg)
    exit(1)

def seek(tokens: list[Token], start_t: int, end_t: int) -> int:
    "Seeks and returns the index of the closing token of a given list."
    if tokens[0].type != start_t:
        return -1
        
    t = 0
    for idx, tok in enumerate(tokens):
        if tok.type == start_t:
            t += 1
        elif tok.type == end_t:
            t -= 1
        if t == 0:
            return idx

    return -1