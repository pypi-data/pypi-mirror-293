import colorama
from colorama import Fore, Style
from itertools import cycle

colorama.init()


def colored_text(text: str, color: str) -> str:
    color_dict = dict(red=Fore.RED, green=Fore.GREEN, yellow=Fore.YELLOW, blue=Fore.BLUE, cyan=Fore.CYAN,
                      magenta=Fore.MAGENTA, white=Fore.WHITE, orange=Fore.LIGHTYELLOW_EX)

    color_code = color_dict.get(color, Fore.WHITE)
    return f"{color_code}{text}{Style.RESET_ALL}"


def rainbow_text(text):
    # 定义彩虹颜色
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    colored_chars = []

    # 为每个字符应用不同的颜色
    for char, color in zip(text, cycle(colors)):
        colored_chars.append(f"{color}{char}")

    return ''.join(colored_chars) + Style.RESET_ALL
