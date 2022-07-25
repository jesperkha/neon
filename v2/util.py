err_count = 0

def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"


def err(msg: str, line: str, start: int, end: int, fatal: bool = False):
    print("| " + line.replace("\n", "\\"))
    print("| " + red(" "*start + "^"*(end-start)))
    print("> " + f"{red('error:')} {msg}")
    print()
    if fatal: exit(1)
    global err_count
    err_count += 1
