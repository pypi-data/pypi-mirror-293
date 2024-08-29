# Tabshot

Tabshot is a script that fetches all URLs from a browser window by iterating over the open tabs. This is achieved in an ineloquent way, but one which should work for most browsers (see [How the script works](#how-the-script-works) for more).

## Requirements

- pyautogui
- pyperclip
- pynput

## Usage and Commands

### print
- prints the list of URLs to the terminal
- usage: `tabshot print` or `tabshot p`

### save
- saves the list of URLs to a json file (see [Output file schema](#output-file-schema))
- usage: `tabshot save <outfile>` or `tabshot s <outfile>`
- add a description: `tabshot s "div centre" -d "useful links for how to centre a div"`
- `outfile` is saved to the `/output` directory

### load
- opens URLs from a saved file in a new (default) browser window
- usage: `tabshot load <infile>` or `tabshot l <infile>`

## Notes

### How the script works

Tabshot uses `pyautogui` to execute keyboard shortcuts to iterate over the browser tabs and copy the URL of each tab. 

Iterating over the browser tabs is performed by using the `ctrl-tab` keyboard shortcut. **Ensure that the browser settings are enabled to allow this behaviour.** 

When two duplicate tab URLs have been encountered, the iteration over browser tabs will cease. 

### Terminating the script

To terminate the script whilst the browser tabs are being iterated over:

1. Provide mouse or keyboard input other than the following keys: `'ctrl'`, `'tab'`, `'c'`, `'v'`, `'t'`, `'l'`, `'enter'`, or
2. Move the mouse to any corner of the screen (this is the default behaviour of `pyautogui`)

## Output file schema
- the `save` command outputs a `json` file to `/output` with the following schema:
```
{
    "title": "",
    "description": "",
    "datetime_created": "",
    "num_urls": "",
    "urls": []
}
```
- `title` corresponds to the argument passed as `outfile` to the `save` command
- input files passed to the `load` command must adhere to this schema in order to be valid


