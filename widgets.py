# ===================== #
# === Onion widgets === #
# ===================== #

import Onion
import Constants as const

class Widget(Onion.Frame): pass # Base class for all widgets.

class Label(Widget):
    def __init__(self,
                 label: str,
                 border: const.BORDER = None) -> None:
        """
        Represents a label.
        -------------------
            label (str) -> the value of the label.
        """
        
        self.label: str = label
        self.isWidget = True
        
    def build(self) -> None:
        """
        Build the label.
        ----------------
        """
        
        size = (
            len(self.label),
            1 + 1
        )
        
        # init / reset the grid
        super().__init__(size, isWidget = True)
        
        # add the label
        for i, le in enumerate(self.label):
            self.grab(i, 0).value = le

class Button(Widget):
    def __init__(self, label: str,
                 callback: callable) -> None:
        """
        Represents a button.
        --------------------
            label (str) -> the value of the button label.
        """
        
        self.label: str = label
        self.isWidget = True
        
        self.parent = None
        
        self.borderType = const.BORDER.LIGHT
    
    def build(self) -> None:
        """
        Build the button.
        -----------------
        """
        
        size = (len(self.label) + 2, 3 + 1)
        
        # init / reset the grid
        super().__init__(size,
                         Onion.Pix('B',
                             isBorder = True,
                             borderType = self.borderType),
                         isWidget = True)
        
        # make the label
        for i, le in enumerate(self.label):
            p = self.grab(i + 1, 1)
            p.value = le
            p.parent = self.parent
            p.isBorder = False # prevent center pixels from being borders

class Entry(Widget): pass

class Radio(Widget): pass

class ListBox(Widget): pass