import colorama
import os
from CupDefs import vars


def perror(text: str):
    print(colorama.Fore.RED + text)


def pwarn(text: str):
    print(colorama.Fore.YELLOW + text)


def pdone(text: str):
    print(colorama.Fore.GREEN + text)


def pinfo(text: str):
    print(colorama.Fore.CYAN + text)


def print_logo():
    with open(os.path.join(vars.PACKAGE_DIR, 'logo'), 'r') as logo:
        logo_text = []
        for line in logo.readlines():
            logo_text.append(line.rstrip('\n'))
        for line in logo_text:
            for s in line:
                if s == 'A':
                    if vars.COLORIZE_PRINT:
                        print(colorama.Back.YELLOW + ' ', end=colorama.Style.RESET_ALL)
                    else:
                        print('#', end='')
                else:
                    print(' ', end='')
            print()
