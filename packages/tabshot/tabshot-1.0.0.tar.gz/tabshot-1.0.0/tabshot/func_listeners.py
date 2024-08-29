import time
import pynput
from pynput.keyboard import KeyCode, Key

def on_mouse_click(x, y, button, pressed):
    return False

def on_keypress(key):
    # print(key)
    key_ = str(key)[2:-1] if hasattr(key, 'char') else key

    if key_ not in {'x0c', 'x03', Key.ctrl_l, Key.tab, 'x14', 'x16', Key.enter}:
        return False
    
def start_mouse_listener():
    mouse_listener = pynput.mouse.Listener(
        on_click=on_mouse_click)
    mouse_listener.start()
    return mouse_listener

def start_keyboard_listener():
    key_listener = pynput.keyboard.Listener(
        on_press=on_keypress)
    key_listener.start()
    return key_listener

def await_enter_keypress():

    flag = False

    def on_press_enter(key):
        global flag
        if key == Key.enter:
            flag = True
        return False

    def check_enter_key():
        global flag
        flag = False
        with pynput.keyboard.Listener(on_press=on_press_enter) as listener:
            listener.join()
        return flag
    
    return check_enter_key()
        