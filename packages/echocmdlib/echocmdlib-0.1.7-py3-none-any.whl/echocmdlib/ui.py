from .colors import colored_text
from rich.status import *
import time
console = Console()

def print_menu(options):
    print(colored_text("请选择一个选项:", 'green'))
    for i, option in enumerate(options, 1):
        print(colored_text(f"{i}. {option}", 'yellow'))


def input_get(text: str):
    print(colored_text(text, "blue"), end="")
    return input()

def waiting(text: str, type: str, func: str):
    with console.status(text, spinner=type):
        eval(func)





