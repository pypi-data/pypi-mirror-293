import json
import time
import pyautogui
import pyperclip
import webbrowser
from .func_listeners import start_mouse_listener, start_keyboard_listener

def session_format_check(session):
    schema = {
        "title": "",
        "description": "",
        "datetime_created": "",
        "num_urls": "",
        "urls": []
    }
    
    try:
        assert set(schema) == set(session) # match properties
        assert isinstance(schema['urls'], list)

        for url in session['urls']:
            assert isinstance(url, str)
        return True

    except AssertionError as error:
        return False

def open_session_from_json(filepath):
    """
    @raise ValueError
    """

    if not filepath.endswith('.json'):
        raise ValueError(f"{filepath} is not a json file")

    with open(filepath, 'r') as file:
        session = json.load(file)
    if not session_format_check(session):
        raise ValueError(f"{filepath} is not correctly formated (see session_format.json")
    return session

def gui_paste_url_in_searchbar(url):
    pyperclip.copy(url)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'v')
    return

def gui_new_tab():
    pyautogui.hotkey('ctrl', 't')
    return

def gui_open_browser_tabs(urls):

    default_url = "https://en.wikipedia.org/wiki/Special:Random"
    webbrowser.open_new_tab(default_url)
    time.sleep(2)

    keyboard_listener = start_keyboard_listener()
    mouse_listener = start_mouse_listener()

    for url in urls:
        if not (mouse_listener.running and keyboard_listener.running):
            raise KeyboardInterrupt("keyboard/mouse interrupt")

        gui_new_tab()
        gui_paste_url_in_searchbar(url)
        time.sleep(0.2)
        pyautogui.hotkey('Enter')

    return True

def execute_load_mode(filepath):
    session = open_session_from_json(filepath)
    urls = session["urls"]
    gui_open_browser_tabs(urls)
    print("done")
