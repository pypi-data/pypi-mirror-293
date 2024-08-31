import sys
sys.dont_write_bytecode =True

a = """Use this tool to facilitate direct, synchronous communication between specialized agents within your agency. When you send a message using this tool, you receive a response exclusively from the designated recipient agent. To continue the dialogue, invoke this tool again with the desired recipient agent and your follow-up message. Remember, communication here is synchronous; the recipient agent won't perform any tasks post-response. You are responsible for relaying the recipient agent's responses back to the user, as the user does not have direct access to these replies. Keep engaging with the tool for continuous interaction until the task is fully resolved. Do not send more than 1 message at a time."""


def print_colored(text, color):
    """
    Prints the given text in the specified color.

    Parameters:
    text (str): The text to be printed.
    color (str): The color to print the text in. Supported colors are:
                 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    """
    # ANSI escape codes for text colors
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'orange': '\033[38;5;208m',
        'pink': '\033[38;5;205m',
        'purple': '\033[38;5;129m',
        'teal': '\033[38;5;37m'
    }

    # Reset code to revert to default color
    reset = '\033[0m'

    # Check if the specified color is supported
    if color in colors:
        print(colors[color] + text + reset)
    else:
        print("Unsupported color! Supported colors are:", ", ".join(colors.keys()))