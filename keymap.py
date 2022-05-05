import kb

class keymap:
    def __init__(self, frame) -> None:
        """
        Represents a key map.
        """
        
        self.frame = frame
        self.map = []
        self.pointer = 0
    
    def move(self, way: str) -> dict:
        """
        """
        
        # Actualize
        self.map = self.frame.widgets
        
        if way in ('up', 'right'):
            if not self.pointer == len(self.map) - 1:
                self.pointer += 1
        
        else:
            if not self.pointer == 0:
                self.pointer -= 1
        
        return self.map[self.pointer]