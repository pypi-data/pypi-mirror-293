from .colors import colored_text
from rich.logging import *
console = Console()
def print_log_IWE(text: str, status: str):
    """

    :type text: str
    """
    if status == "info":
        print(colored_text("[INFO]","green"), end = "")
        console.log(text)
    if status == "warn":
        print(colored_text("[WARN]", "orange"), end="")
        console.log(text)
    if status == "error":
        print(colored_text("[ERROR]","red"), end = "")
        console.log(text)