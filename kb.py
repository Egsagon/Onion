# ======================= #
# === Onion kb module === #
# ======================= #

import os
import Utils
import threading
from copy import copy
import Constants as const
from keyboard import is_pressed
from pynput import keyboard as keyb

class inputSTR:
    def __init__(self,
                 done: callable,
                 mode: callable,
                 stoppers: list = ['enter']) -> None:
        """
        Represents an input instance.
        -----------------------------
            done (fn) -> function to call when finished.
            mode (fn) -> functin to call when value moded.
            stoppers (list) -> list of stop keys.
            cursor (bool) -> wether to enable cursor output or not.
        """
        
        self.value: list = []
        self.cursor = 0
        
        self.done: callable = done
        self.mode: callable = mode
        self.stoppers: list = stoppers
        
        print('Listenning STR input.')
    
    def output(self) -> str:
        """
        Output the current input string.
        --------------------------------
        """
        
        # cursorChar = '\033[91m|\033[0m'
        
        # cursed = copy(self.value)
        # cursed.insert(self.cursor, self.cursorChar)
        # return ''.join(cursed) # Simple | cursor
        
        # return ''.join(self.value) # without cursor
        
        cursed = copy(self.value)
        cursed.append(' ')
        cursed[self.cursor] = '\033[1;0;7m' + cursed[self.cursor] + '\033[1;0;0m'
        return ''.join(cursed)
        
    def next(self, key, isMod) -> None:
        """
        Decide how to handle a key press.
        ----------------------------------
            key (str) -> the presed key.
            isMod (bool) -> wheter the key is a mod.
        """
        
        oldOutput = self.output()
        
        # Check for key stopper
        if key in self.stoppers:
            self.done(''.join(self.value))
            # TODO: destroy instance
        
        # Check for mods
        if isMod:
            # Check for special keys
            if key == 'space':
                self.value.insert(self.cursor, ' ')
                self.cursor += 1
                
            elif key == 'backspace':
                
                if len(self.value) and self.cursor:
                    self.value.pop(self.cursor - 1 -
                        int(self.cursor == len(self.value) + 1))
                    
                    self.cursor -= 1
            
            elif key == 'left':
                if not self.cursor == 0: self.cursor -= 1
            elif key == 'right':
                if not self.cursor == len(self.value): self.cursor += 1
            
            elif key == 'home': self.cursor = 0
            elif key == 'end': self.cursor = len(self.value)
        
        # Normal keys
        else:
            if Utils.isCaps():
                # Uppercase
                if key in const.alpha: key = key.upper()
                
                # Numbers
                elif key in const.nums:
                    key = str(const.nums.index(key) + 1)
                    if len(key) == 2: key = '0' # Prevent 10
            
            if key == '""': key = 'ˊ' # Prevent ""
            
            # Append
            self.value.insert(self.cursor, key)
            self.cursor += 1
            
            # TODO: handle Alt+ chars.
        
        # call user function
        if oldOutput != self.output(): self.mode(self.output())

class inputBOOL:
    def __init__(self,
                 done: callable,
                 mode: callable,
                 default: bool = False,
                 stoppers: list = ['enter']) -> None:
        """
        Represents an input instance.
        -----------------------------
            done (fn) -> function to call when finished.
            mode (fn) -> functin to call when value moded.
            stoppers (list) -> list of stop keys.
            cursor (bool) -> wether to enable cursor output or not.
        """
        
        self.value: bool = default
        
        self.done: callable = done
        self.mode: callable = mode
        self.stoppers: list = stoppers
        
        print('Listenning BOOL input.')
    
    def output(self) -> str:
        """
        Output the current input boolean.
        --------------------------------
        """
        
        return self.value
        
    def next(self, key, isMod) -> None:
        """
        Decide how to handle a key press.
        ----------------------------------
            key (str) -> the presed key.
            isMod (bool) -> wheter the key is a mod.
        """
        
        if key in self.stoppers:
            self.done(self.output())
            # TODO: destroy instance
        
        oldValue = self.value
        
        if key == 'space': self.value = not self.value
        
        elif key in ('left', 'down'): self.value = False
        elif key in ('right', 'up'): self.value = True
        
        if oldValue != self.value: self.mode(self.output())

class inputINT:
    def __init__(self,
                 done: callable,
                 mode: callable,
                 default: int = 0,
                 stoppers: list = ['enter']) -> None:
        """
        Represents an input instance.
        -----------------------------
            done (fn) -> function to call when finished.
            mode (fn) -> functin to call when value moded.
            stoppers (list) -> list of stop keys.
            cursor (bool) -> wether to enable cursor output or not.
        """
        
        self.value: int = default
        
        self.done: callable = done
        self.mode: callable = mode
        self.stoppers: list = stoppers
        
        print('Listenning INT input.')
    
    def output(self) -> str:
        """
        Output the current input boolean.
        --------------------------------
        """
        
        return self.value
        
    def next(self, key, isMod) -> None:
        """
        Decide how to handle a key press.
        ----------------------------------
            key (str) -> the presed key.
            isMod (bool) -> wheter the key is a mod.
        """
        
        if key in self.stoppers:
            self.done(self.output())
            # TODO: destroy instance
        
        oldValue = self.value
        
        if key in ('left', 'down'): self.value -= 1
        elif key in ('right', 'up'): self.value += 1
        
        if oldValue != self.value: self.mode(self.output())


class KB:
    def __init__(self,
                 callback: callable = None,
                 errorCallback: callable = None,
                 stopCallback: callable = None) -> None:
        """
        Listen to the leyboard.
        """
        
        self.cb: callable = callback
        self.errorcb: callable = errorCallback
        self.stopcb: callable = stopCallback

        # List of bindings
        self.bindings = {}
        
        # Current user input.
        self.currentInput: classmethod = None

    def bind(self, key: str, callback: callable) -> None:
        """
        Bind a key to a function.
        -------------------------
        """
        
        self.bindings[str(key)] = callback
    
    def unbind(self, key: str) -> None:
        """
        Unbind a key from a function.
        -----------------------------
        """
        
        self.bindings.pop(str(key))

    def input(self, whenDone: callable,
              whenMod: callable,
              stops: list = ['enter']) -> None:
        """
        Ask the user for an input.
        --------------------------
            whenDone (fn) -> function to call when finished.
            whenmod (fn) -> function to call when modified.
            stops (list) -> a list of stoppers.
        """
        
        self.currentInput = inputSTR(whenDone, whenMod, stops) # hum: was no stop

    def inputBool(self,
                  whenDone: callable,
                  whenMod: callable,
                  default: bool = False,
                  stops: list = ['enter']) -> None:
        """
        Ask the user for a bool input.
        ------------------------------
            whenDone (fn) -> function to call when finished.
            whenmod (fn) -> function to call when modified.
            default (bool) -> default value.
            stops (list) -> a list of stoppers.
        """
        
        self.currentInput = inputBOOL(whenDone, whenMod, default, stops)

    def inputInt(self,
                 whenDone: callable,
                 whenMod: callable,
                 default: int = 0,
                 stops: list = ['enter']) -> None:
        """
        Ask the user for an int input.
        ------------------------------
            whenDone (fn) -> function to call when finished.
            whenmod (fn) -> function to call when modified.
            default (int) -> default value.
            stops (list) -> a list of stoppers.
        """
        
        self.currentInput = inputINT(whenDone, whenMod, default, stops)

    def listen(self, key: str, isMod: bool) -> None:
        """
        Manage incoming key events.
        ---------------------------
            key (str) -> key code.
            isMod (bool) -> wheter the key is a mod.
        """
        
        # Check bindings
        if key in self.bindings.keys(): self.bindings[key]()
        
        # Check for user input
        if self.currentInput is not None: self.currentInput.next(key, isMod)
        
        # Call user function
        else: self.cb(key, isMod)

    def start(self) -> None:
        """
        Starts listenning the keyboard.
        -------------------------------
        """
        
        try:
            Utils.allowKeyboard(False)
            
            with keyb.Listener(
                on_press = lambda k: self.listen(*Utils.parse(k))
            ) as ln: ln.join()
            
            Utils.allowKeyboard(True)
        
        except KeyboardInterrupt:
            if self.stopcb is None:
                Utils.allowKeyboard()
                exit('Process interrupted.')
            
            self.stopcb
        
        except Exception as e:
            if self.errorcb is None:
                Utils.allowKeyboard()
                raise e
            
            self.errorcb
        
        Utils.allowKeyboard(True)
        print('Proccess finished.')

    def startAsThread(self) -> None:
        """
        Starts the Listener as a separated thread.
        ------------------------------------------
        """
        
        threading.Thread(target = self.start).start()


"""
def main(k, i): print(k, i)
def done(r): print('Input ended with value', r)

def mod(r):
    os.system('clear')
    print(r)

kb = KB(main)
kb.inputInt(done, mod)

kb.start()
"""