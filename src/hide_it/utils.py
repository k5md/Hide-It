import os
import json
import win32api
import win32gui
import win32con
from PIL import ImageColor
from typing import Union
import tkinter as tk

def apply_to_widget_and_children(widget: tk.Widget, fn):
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

def enable_clickthrough(hwnd, color_key = 0, alpha = 255):
    # NOTE: to get color_key, use win32api.RGB
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)
    win32gui.SetLayeredWindowAttributes(hwnd, color_key, alpha, win32con.LWA_ALPHA)

def disable_clickthrough(hwnd):
    win32api.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 0)

def make_draggable(widget: tk.Widget, grip: tk.Widget):
    press_x = None
    press_y = None

    def handle_press(event):
        nonlocal press_x, press_y
        press_x = event.x
        press_y = event.y

    def handle_drag(event):
        dx = event.x - press_x
        dy = event.y - press_y
        x = widget.winfo_x() + dx
        y = widget.winfo_y() + dy
        widget.geometry(f"+{x}+{y}")

    grip.bind("<Button-1>", handle_press)
    grip.bind("<B1-Motion>", handle_drag)

def make_resizable(widget: tk.Widget, grip: tk.Widget, side: Union[tk.SE, tk.NW, tk.NE, tk.SW]):
    def resize(event):
        min_w = widget.minsize()[0]
        min_h = widget.minsize()[1]
        (x0, y0, x1, y1) = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_pointerx(), widget.winfo_pointery())
        # offsets from mouse to window
        dx = x1 - x0 
        dy = y1 - y0
        if side == tk.SE: (x, y, w, h) = (x0, y0, dx, dy)
        elif side == tk.NW: (x, y, w, h) = (x1, y1, widget.winfo_width() - dx, widget.winfo_height() - dy)
        elif side == tk.NE: (x, y, w, h) = (x1 - dx, y1, dx, widget.winfo_height() - dy)
        elif side == tk.SW: (x, y, w, h) = (x1, y1 - dy, -dx + widget.winfo_width(), dy)
        # prevent window from moving
        if (w < min_w): (x, w) = (x0, min_w)
        if (h < min_h): (y, h) = (y0, min_h)
        widget.geometry(f"{w}x{h}+{x}+{y}")

    grip.bind("<B1-Motion>", resize)
