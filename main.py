import Onion, kb, widgets, keymap
import Constants as const

def callback(): print('Button pressed.')

frame = Onion.Frame()
keymap = keymap.keymap(frame)

label = widgets.Label('label')
btn = widgets.Button('Button 0', callback)
btn1 = widgets.Button('Button 1', callback)

frame.add(0, -3, label, 'center')
frame.add(-6, 0, btn, 'center')
frame.add(6, 0, btn1, 'center')

def main(key, isMod):
    if key in ('left', 'right', 'down', 'up'):
        focusedWidget = keymap.move(key)
        
        coords = focusedWidget['coords']
        widg = focusedWidget['widget']
        
        if isinstance(widg, widgets.Button):
            # Focus
            widg.borderType = const.BORDER.DOUBLE
    
    point = keymap.pointer
    print(point)
    label.label = str(point)
    frame.bake(False)


k = kb.KB(main)
k.start()