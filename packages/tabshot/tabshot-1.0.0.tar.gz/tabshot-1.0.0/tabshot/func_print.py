import time
import pyautogui
import pyperclip
from .func_listeners import start_keyboard_listener, start_mouse_listener, await_enter_keypress

def print_instructions():
    instructions = [
        "\n  Instructions  ",
        "----------------",
        "1. Read all instructions below first",
        "2. Navigate to web browser",
        "3. Deselect any text/buttons",
        "4. Press the \"ENTER\" key", 
        "5. Wait for the script to iterate over all browser tabs; any mouse/keyboard input during this time will terminate the script",
        "\nAwaiting \"ENTER\" keypress..."
    ]

    print('\n'.join(instructions), end='\n\n')
    return

def gui_get_url_from_addressbar():
    """
    Returns the url of the current tab in the browser window.
    The web browser window must be the top-most application 
    window. 
    """
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()

def gui_move_to_next_tab():
    pyautogui.hotkey('ctrl', 'tab')
    return

def gui_iter_browser_tabs():
    """
    Iterates over browser tabs to get each tab url.
    Raises Exception if keyboard or mouse input is detected.
    """

    saved_urls = set()
    repeat_url_count = 0
    default_clipboard = "empty"

    keyboard_listener = start_keyboard_listener()
    mouse_listener = start_mouse_listener()

    while repeat_url_count < 2:
        
        pyperclip.copy(default_clipboard)
        current_url = gui_get_url_from_addressbar()

        if not (mouse_listener.running and keyboard_listener.running):
            raise Exception("keyboard/mouse interrupt")

        if current_url in saved_urls:
            repeat_url_count += 1
        elif current_url != default_clipboard:
            saved_urls.add(current_url)
        gui_move_to_next_tab()
        time.sleep(0.2)
    
    return saved_urls

def print_to_terminal(urls):
    print(f"\n  URLs (n={len(urls)})  ",
        "-"*(13+len(str(len(urls)))), sep='\n')

    for u in urls:
        print(u)
    return
    
def execute_print_mode():
    
    print_instructions()
    if not await_enter_keypress():
        raise ValueError("\"ENTER\" was not pressed")

    urls = gui_iter_browser_tabs()
    print_to_terminal(urls)
    
    return urls
