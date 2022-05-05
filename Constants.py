# ======================= #
# === Onion constants === #
# ======================= #

alpha = 'abcdefghijklmnopqrstuvwxyz'
nums = '&é"ˬ(-è_çà'

class ORIGIN:
    CENTER = 'center'
    TOPLEFT = 'top left'

class CHAR:
    CIRCLE = ['○', '◔', '◐', '◕', '◉', '●']
    SQUARE = ['□', '▣', '■']
    FULL = '█'

class STATE:
    UNFOCUSED = 'unfocused'
    FOCUSED   = 'focused'
    ACTIVATED = 'activated'

class BORDER:
    def get(type: set, style) -> str:
        """
        Returns the appropriate char.
        -----------------------------
            type: (set) -> the received set.
            style (BORDER) -> a list from the BORDER lists.
        Returns the appropriate str.
        """
        
        return style[BORDER.INDEX[frozenset(type)]]
    
    INDEX = {
        frozenset({'left', 'right', 'up', 'down'}): 0,
        
        frozenset({'left', 'right', 'up'}): 1,
        frozenset({'left', 'right', 'down'}): 2,
        frozenset({'left', 'up', 'down'}): 3,
        frozenset({'right', 'up', 'down'}): 4,
        
        frozenset({'left', 'up'}): 5,
        frozenset({'right', 'up'}): 6,
        frozenset({'left', 'down'}): 7,
        frozenset({'right', 'down'}): 8,
        
        frozenset({'left', 'right'}): 9,
        frozenset({'up', 'down'}): 10
    }
    
    HEAVY = ['╋', '┻', '┳', '┫', '┣', '┛', '┗', '┓', '┏', '━', '┃']
    
    LIGHT = ['┼', '┴', '┬', '┤', '├', '┘', '└', '┐', '┌', '─', '│']
    
    DOUBLE =['╬', '╩', '╦', '╣', '╠', '╝', '╚', '╗', '╔', '═', '║']
    
    ROUND = ['┼', '┴', '┬', '┤', '├', '╯', '╰', '╮', 'M', '─', '│']
