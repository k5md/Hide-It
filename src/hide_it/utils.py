from PIL import ImageColor

def apply_to_widget_and_children(widget, fn):
    fn(widget)
    for child in widget.winfo_children():
        apply_to_widget_and_children(child, fn)            

def find_matching_color(color):
    (r, g, b) = ImageColor.getcolor(color, "RGB")
    # taken from https://stackoverflow.com/a/3943023/112731
    return '#000000' if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else '#FFFFFF'
  