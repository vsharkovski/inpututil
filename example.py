"""When you open notepad and you press F while the notepad window is active,
It will detect it and print to indicate it."""
import importutil

def onPressF():
    """example"""
    print('pressed F!')

iu = inpututil.InputUtil()
iu.set_active_window('Untitled - Notepad') #make it so it only detects keys when this window is active
iu.bind_hotkey(keys=inpututil.VK['KEY_F'], func=onPressF) #bind the hotkey

iu.start() #start main loop
