import Onion, widgets, kb, keymap

frame = Onion.Frame()
km = keymap.keymap(frame)

lab = widgets.Label('/')

btn1 = widgets.Button('Button 1', None)
btn2 = widgets.Button('Button 2', None)

frame.add(-6, 0, btn1, 'center')
frame.add(6, 0, btn2, 'center')
frame.add(0, -6, lab, 'center')

def main(key, isMod):
    lab.label = str(km.pointer)
    
    if key in ('left', 'down', 'up', 'right'): km.move(key)
    
    frame.bake()

k = kb.KB(main)
k.start()