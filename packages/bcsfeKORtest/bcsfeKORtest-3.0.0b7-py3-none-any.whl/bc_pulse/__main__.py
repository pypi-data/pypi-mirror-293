import sys
from colorama import init, Fore, Style
import bc_pulse
from bc_pulse import cli, checkKey

checkKey.start()


args = sys.argv[1:]
for arg in args:
    if arg.lower() in ["--version", "-v"]:
        print(bc_pulse.__version__)
        exit()

