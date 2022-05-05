# ======================= #
# === Onion utilities === #
# ======================= #

import os
# import Onion

def fetchtermSize() -> list:
    """
    Attempts to fetch the length/width of the terminal.
    ---------------------------------------------------
    Returns a list containing the X/Y length.
    """
    
    return list(
        map(int, os.popen('stty size').read().split())
    )[::-1]
    
    # Note: List is inverted because stty counts in rows / cols
    # and not in x / y unit.

def parse(code) -> tuple:
    """
    Parse the keycode.
    ------------------
    Returns the key name and wheter its a mod.
    """
    
    key = str(code).replace('Key.', '').replace('\'', '')
    isMod = 'Key' in str(code)
    
    return key, isMod

def fetchBorderPixels(pix) -> set:
    """
    Search for borders around the given pixel.
    ------------------------------------------
        pix (Pix) -> the current pixel.
    Returns a set of strings.
    """
    
    # Filter to test if a pixel exists and is a border
    # isBorder = lambda p: p is not None and pix.isBorder
    
    def isBorder(c):
        p = pix.parent.grab(*c)
        if p is None: return False
        return p.isBorder
    
    # Get our pixel's coordinatess
    x, y = pix.parent.findPix(pix)
    
    # Create the coordinates
    around = {(x - 1, y): 'left', (x + 1, y): 'right',
              (x, y - 1): 'up', (x, y + 1): 'down'}
    
    # Make the set
    return {v for k, v in around.items() if isBorder(k)}

def allowKeyboard(do: bool = True) -> None:
    """
    Allow or disallow the input on a terminal.
    ------------------------------------------
        do (bool) -> Choose wether.
    """
    
    os.system('stty ' + ('-echo -icanon time 0 min 0', 'echo icanon')[do])

def isCaps() -> bool:
    """
    Returns wheter the caps are locked or not.
    ------------------------------------------
    """
    
    return bool(int(os.popen('xset q | grep LED').read()[-2]))

# /