import os
import json
import win32api
import win32gui
import win32con
from PIL import ImageColor

def apply_to_widget_and_children(widget, fn):
    fn(widget)
    for child in widget.winfo_children():
        apply_to_widget_and_children(child, fn)            

def find_matching_color(color):
    (r, g, b) = ImageColor.getcolor(color, "RGB")
    # taken from https://stackoverflow.com/a/3943023/112731
    return '#000000' if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else '#FFFFFF'

def load_json(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            payload = json.loads(content)
            return payload

def save_json(file_path, payload):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(payload, file, ensure_ascii=False)

def enable_clickthrough(hwnd):
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)

def disable_clickthrough(hwnd):
    win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 0)