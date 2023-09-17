# Todo: rework error system (doing)

import os
if os.name == "nt":
    os.system("color")

def err(msg: str):
    print(f"{red('error: ')}{msg}")
    exit(1)

def warn(msg: str):
    print(f"{yellow('warning: ')}{msg}")

def red(text: str) -> str:
    return f"\033[91m{text}\033[0m"

def yellow(text: str) -> str:
    return f"\033[33m{text}\033[0m"

def green(text: str):
    return f"\033[32m{text}\033[0m"


def syntax_error(msg: str, line: int, start: int, end: int, string: str):
    print(f"{red('error:')} {msg}, line {line}")
    print(f" {line} | " + string.replace("\n", "").replace("\t", 4*" "))
    diff = end-start if end != start else 1
    print(f" {len(str(line))*' '} | " + red(" "*start + "^"*diff))
    print()

