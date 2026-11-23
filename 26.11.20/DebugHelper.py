class color:
    green = "\033[92m"
    red = "\033[91m"
    yellow = "\033[93m"
    blue = "\033[94m"
    white = "\033[0m"
    pink = "\033[95m"
    teal = "\033[96m"


def log(message: str, col: str = color.white) -> None:
    print(f"{col}Log : {message}{color.white}")