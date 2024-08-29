from .colors import colored_text
from rich.console import Console
from rich.text import Text

def print_log_IWE(text: str, status: str):
    """

    :type text: str
    """
    if status == "info":
        print(colored_text("[INFO]","green"), end = "")
        print(text)
    if status == "warn":
        print(colored_text("[WARN]", "orange"), end="")
        print(text)
    if status == "error":
        print(colored_text("[ERROR]","red"), end = "")
        print(text)