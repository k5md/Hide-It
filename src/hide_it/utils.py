import os
import json
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