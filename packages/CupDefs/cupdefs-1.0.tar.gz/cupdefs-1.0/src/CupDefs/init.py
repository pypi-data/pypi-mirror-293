import colorama
from CupDefs import utils
from CupDefs import vars
from CupDefs import vergen


def init(*args):
    if 'no_color_init' not in args:
        colorama.init(autoreset=True)
    if not vars.COLORIZE_PRINT:
        utils.pwarn = utils.pdone = utils.perror = utils.pinfo = print
    if 'no_vergen_init' not in args:
        vergen.init_vergen()
    if 'no_logo' not in args:
        utils.print_logo()
