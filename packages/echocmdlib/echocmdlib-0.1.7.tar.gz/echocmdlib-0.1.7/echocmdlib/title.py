import pyfiglet
from rich.console import Console
from rich.text import Text

console = Console()


def generate_gradient_text(text):
    ascii_art = pyfiglet.figlet_format(text)
    lines = ascii_art.splitlines()
    gradient_text = Text()

    max_x = max(len(line) for line in lines)
    max_y = len(lines)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            # 根据x和y的比例决定颜色，形成渐变
            ratio = (x + y) / (max_x + max_y)
            if ratio < 0.2:
                color = "red"
            elif ratio < 0.4:
                color = "yellow"
            elif ratio < 0.6:
                color = "green"
            elif ratio < 0.8:
                color = "cyan"
            else:
                color = "magenta"

            gradient_text.append(char, style=color)
        gradient_text.append("\n")

    return gradient_text


def print_title(text):
    gradient_art = generate_gradient_text(text)
    console.print(gradient_art)