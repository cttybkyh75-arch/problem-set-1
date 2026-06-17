

import sys
import random
from pyfiglet import Figlet

def main():
    figlet = Figlet()
    available_fonts = figlet.getFonts()
    if len(sys.argv) == 1:
        font_name = random.choice(available_fonts)
        figlet.setFont(font=font_name)
    elif len(sys.argv) == 3:
        flag = sys.argv[1]
        font_name = sys.argv[2]
        if flag not in ["-f", "--font"]:
            sys.exit("Invalid usage. First argument must be -f or --font.")
        if font_name not in available_fonts:
            sys.exit(f"Error: '{font_name}' is not a recognized font name.")
            
        figlet.setFont(font=font_name)
    else:
        sys.exit("Usage: python figlet.py OR python figlet.py -f <font_name>")
    user_text = input("Input: ")
    print("\nOutput:")
    print(figlet.renderText(user_text))

main()