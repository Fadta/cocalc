from enum import Enum

class TextColor(Enum):
    """
    ANSI scape sequences for colors,
    when using a constant call the value
    (TextColor.const.value)

    call TextColor.ENDC so escape sequence is terminated
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorify(text, color:TextColor):
    return f"{color.value}{text}{TextColor.ENDC.value}"

if __name__ == "__main__":
    print(colorify("HEADER", TextColor.HEADER))
    print(colorify("OKBLUE", TextColor.OKBLUE))
    print(colorify("OKCYAN", TextColor.OKCYAN))
    print(colorify("OKGREEN", TextColor.OKGREEN))
    print(colorify("WARNING", TextColor.WARNING))
    print(colorify("FAIL", TextColor.FAIL))
    print(colorify("BOLD", TextColor.BOLD))
    print(colorify("UNDERLINE", TextColor.UNDERLINE))

