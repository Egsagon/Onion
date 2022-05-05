# ==================== #
# === Onion module === #
# ==================== #

import os
import Utils
from Errors import *
from typing import Union
import Constants as const
from copy import copy, deepcopy

# ==== Grid pixel ==== #
class Pix(object):
    def __init__(self,
                 value: str,
                 isBorder: bool = False,
                 borderType: const.BORDER = None,
                 parent = None) -> None:
        """
        Represents a pixel.
        -------------------
        """
        
        self.value = value
        self.isBorder = isBorder
        self.borderType = borderType or const.BORDER.LIGHT
        self.parent = parent
    
    def bake(self) -> str:
        """
        Bake the pixel.
        ---------------
        Returns a string containing the baked pixel (warning, it's hot).
        """
        
        if self.isBorder:
            _set = Utils.fetchBorderPixels(self)
            return const.BORDER.get(_set, self.borderType)
        
        return self.value


# === Onion Frame ==== #
class Frame:
    def __init__(self,
                 size: tuple = None,
                 pix: Pix = None,
                 isWidget: bool = False) -> None:
        """
        Represents a Frame.
        -------------------
        """
        
        self.size = size or Utils.fetchtermSize()
        self.isWidget = isWidget
        self.widgets = []
        pix = pix or Pix(' ')
        pix.parent = self
        
        # Error protection
        if len(self.size) != 2:
            raise SizeErr(f'Invalid size: {self.size}')
        
        # Making the grid
        self.grid = [[deepcopy(pix) for _ in range(self.size[0])]
                     for _ in range(self.size[1] - 1)]
    
    def buildWidget(self, x: int, y: int, widget, of: const.ORIGIN) -> None:
        """
        Build a widget.
        """
        
        widget.build()
        
        abs, ord = self.getAxis(of)
        
        # Correct coordinates if origin is centered
        addX, addY = 0, 0
        if abs == 'center': addX -= widget.size[1] // 2
        if ord == 'center': addY -= widget.size[0] // 2
        
        if ord == 'right':
            for i, l in enumerate(widget.grid):
                widget.grid[i] = widget.grid[i][::-1]

        for iy, line in enumerate(widget.grid):
            for ix, pix in enumerate(line):
                pix.parent = self
                coords = (x + ix + addY, y + iy + addX)
                coords = self.getOrigin(*coords, of)
                self.grid[coords[1]][coords[0]] = pix
    
    def bake(self, erase: bool = True) -> None:
        """
        Bake the frame.
        """
        
        # Build the widgets.
        for widget in self.widgets:
            x, y, of = widget['coords']
            self.buildWidget(x, y, widget['widget'], of)
        
        if erase: os.system('clear')
        
        li = '\n'
        
        print(
            li.join(map(lambda l: ''.join(
                    map(lambda p: p.bake(), l)), self.grid))
        )
        
    def getAxis(self, of: const.ORIGIN) -> tuple:
        """
        Parse user axis to readable origin.
        """
        of = of or 'top left' # case None is passed
        
        if ' ' in of: abs, ord = of.split(' ')
        elif of == 'center': abs, ord = 'center', 'center'
        else: raise OriginErr(f'Invalid origin: {of}')
        
        return abs, ord
    
    def getOrigin(self, x: int, y: int, of: const.ORIGIN = None) -> tuple:
        """
        Fix the coordinates depending on the origin.
        --------------------------------------------
            x (int) / y (int) -> coords.
            of (ORIGIN) -> the origin.
        Returns a tuple containing new coords.
        """
        
        x, y = map(int, (x, y))
        
        # Inverting axis because we say 'top left'
        # and not 'left top'
        ord, abs = self.getAxis(of)
        
        if abs == 'left': pass
        elif abs == 'center': x -= self.size[0] // 2 + 1
        elif abs == 'right': x = self.size[0] - x - 1
        
        if ord == 'top': pass
        elif ord == 'center': y -= self.size[1] // 2 + 1
        elif ord == 'bottom': y = self.size[1] - y - 2
        
        return x, y
    
    def grab(self, x: int, y: int, of: const.ORIGIN = None) -> Pix:
        """
        Returns a modifiable pixel from the grid.
        -----------------------------------------
            x (int) / y (int) -> coords.
            of (ORIGIN) -> the origin the coords are from.
        Returns a modifiable Pix instance,
        or None if no pixel found.
        """
        
        x, y = self.getOrigin(x, y, of)
        try: return self.grid[y][x]
        except: return None

    def add(self, x: int, y: int, frame, of: const.ORIGIN = None) -> None:
        """
        Append a frame to the main one.
        --------------------------------
            x (int) / y (int) -> coords.
            frame (Frame) -> the frame to append.
            of (ORIGIN) -> origin the coords are from.
        """
        
        if frame.isWidget:
            self.widgets.append({'coords': (x, y, of), 'widget': frame})
        else:
            pass
        
        """
        if frame.isWidget: frame.build()
        
        abs, ord = self.getAxis(of)
        
        # Correct coordinates if origin is centered
        addX, addY = 0, 0
        if abs == 'center': addX -= frame.size[1] // 2
        if ord == 'center': addY -= frame.size[0] // 2
        
        if ord == 'right':
            for i, l in enumerate(frame.grid):
                frame.grid[i] = frame.grid[i][::-1]
                # TODO: fix

        for iy, line in enumerate(frame.grid):
            for ix, pix in enumerate(line):
                pix.parent = self
                coords = (x + ix + addY, y + iy + addX)
                coords = self.getOrigin(*coords, of)
                self.grid[coords[1]][coords[0]] = pix
        """

    def findPix(self, pix: Pix) -> tuple:
        """
        Attempts to get the coordinates of a pixel.
        -------------------------------------------
            pix (Pix) -> the pixel.
        Returns a tuple of coordinates or None if the pixel
        is not found.
        """
        
        for y, line in enumerate(self.grid):
            for x, pixel in enumerate(line):
                if pix == pixel: return x, y

