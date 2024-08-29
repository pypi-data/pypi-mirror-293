import os
import json
from datetime import datetime
from .func_listeners import await_enter_keypress
from .func_print import gui_iter_browser_tabs, print_instructions

def new_session(title, urls, description):
    return {
        "title": title,
        "description": description,
        "datetime_created": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
        "num_urls": len(urls),
        "urls": list(urls)
    }

def write_session_to_json(session):
    dest_filename = session["title"] + ".json"
    dest_filepath = os.path.join("output", dest_filename)

    if not os.path.exists('output'):
        os.mkdir('output')

    with open(dest_filepath, 'w', encoding='utf-8') as f:
        json.dump(session, f, ensure_ascii=False, indent=4)
    return 0

def execute_save_mode(title, description):

    print_instructions()
    if not await_enter_keypress():
        raise ValueError("\"ENTER\" was not pressed")

    urls = gui_iter_browser_tabs()
    session = new_session(title=title,urls=urls,description=description)
    write_session_to_json(session)

    print("done")