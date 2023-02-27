import tkinter as tk
import re
from functools import partial

from hide_it.utils import apply_to_widget_and_children, find_matching_color
from hide_it.libs.ResizeGrip import ResizeGrip

class Overlay(tk.Toplevel):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    MIN_SIZE = (80, 64)

    @staticmethod
    def change_background_color(widget, color, highlight_color):
        if type(widget) is ResizeGrip:
            widget.config(background = color)
        if type(widget) is tk.Label:
            widget.config(background = color)
        elif type(widget) is tk.Entry:
            widget.config(
                background = color,
                disabledbackground = color,
                readonlybackground = color,
                selectbackground = highlight_color,
            )

    @staticmethod
    def change_foreground_color(widget, color):
        if type(widget) is ResizeGrip:
            widget.change_resize_grip_color(color)
        if type(widget) is tk.Label:
            widget.config(foreground = color)
        elif type(widget) is tk.Entry:
            widget.config(
                disabledforeground = color,
                foreground = color,
                insertbackground = color,
                selectforeground = color,
            )

    def __init__(self, *args, overlay_color = "#000", overlay_geometry = "0x0+0+0", overlay_close_handler = lambda event: None, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        self.overlay_color = overlay_color
        self.overlay_color_string_var = tk.StringVar(value = self.overlay_color)

        # CREATE WIDGETS
        self.root_frame = tk.Frame(self)

        self.top_frame = tk.Frame(self.root_frame)
        self.top_left_resize_grip = ResizeGrip(self.top_frame, resize_grip_angle = 180)
        self.close_label = tk.Label(self.top_frame, text="x")
        self.top_right_resize_grip = ResizeGrip(self.top_frame, resize_grip_angle = 90)

        self.center_frame = tk.Frame(self.root_frame)
        self.position_grip = tk.Label(self.center_frame)

        self.bottom_frame = tk.Frame(self.root_frame)
        self.bottom_left_resize_grip = ResizeGrip(self.bottom_frame, resize_grip_angle = 270)
        self.overlay_color_entry = tk.Entry(self.bottom_frame, textvariable = self.overlay_color_string_var, width = 8, justify = tk.CENTER, bd = 0, highlightthickness = 0)
        self.bottom_right_resize_grip = ResizeGrip(self.bottom_frame, resize_grip_angle = 0)

        # PACK WIDGETS
        self.top_left_resize_grip.pack(side = tk.LEFT, fill = tk.BOTH)
        self.close_label.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.top_right_resize_grip.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.top_frame.pack(side = tk.TOP, fill = tk.BOTH)

        self.position_grip.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.center_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.bottom_left_resize_grip.pack(side = tk.LEFT, fill = tk.BOTH)
        self.overlay_color_entry.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.bottom_right_resize_grip.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.bottom_frame.pack(side = tk.BOTTOM, fill = tk.BOTH)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # REGISTER LISTENERS
        self.top_left_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.TOP_LEFT))
        self.close_label.bind("<Button-1>", overlay_close_handler)
        self.top_right_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.TOP_RIGHT))

        self.position_grip.bind("<Button-1>", self.handle_press)
        self.position_grip.bind("<B1-Motion>", self.handle_drag)

        self.bottom_left_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.BOTTOM_LEFT))
        self.overlay_color_string_var.trace_add("write", lambda *args, **kwargs: self.handle_color())
        self.bottom_right_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.BOTTOM_RIGHT))

        # CONFIGURE WIDGETS
        self.overrideredirect(True)
        self.minsize(*Overlay.MIN_SIZE)
        self.geometry(overlay_geometry)
        self.attributes("-topmost", True)
        self.update()

        self.handle_color()

    def handle_color(self):
        color = self.overlay_color_string_var.get()
        color_valid = re.search(r'^#([0-9a-fA-F]{3}){1,2}$', color)
        if not color_valid:
            return
        self.overlay_color = color
        apply_to_widget_and_children(self, partial(Overlay.change_background_color, color = self.overlay_color, highlight_color = "#7F7F7F"))
        matching_color = find_matching_color(self.overlay_color)
        apply_to_widget_and_children(self, partial(Overlay.change_foreground_color, color = matching_color))
        self.update()

    def handle_press(self, event):
        self.press_x = event.x
        self.press_y = event.y

    def handle_drag(self, event):
        dx = event.x - self.press_x
        dy = event.y - self.press_y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}")

    def resize(self, event, side):
        min_w = self.minsize()[0]
        min_h = self.minsize()[1]
        (x0, y0, x1, y1) = (self.winfo_rootx(), self.winfo_rooty(), self.winfo_pointerx(), self.winfo_pointery())
        # offsets from mouse to window
        dx = x1 - x0 
        dy = y1 - y0
        if side == Overlay.BOTTOM_RIGHT: (x, y, w, h) = (x0, y0, dx, dy)
        if side == Overlay.TOP_LEFT: (x, y, w, h) = (x1, y1, self.winfo_width() - dx, self.winfo_height() - dy)
        if side == Overlay.TOP_RIGHT: (x, y, w, h) = (x1 - dx, y1, dx, self.winfo_height() - dy)
        if side == Overlay.BOTTOM_LEFT: (x, y, w, h) = (x1, y1 - dy, -dx + self.winfo_width(), dy)
        # prevent window from moving
        if (w < min_w): (x, w) = (x0, min_w)
        if (h < min_h): (y, h) = (y0, min_h)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def serialize(self):
        return { "overlay_color": self.overlay_color, "overlay_geometry": self.winfo_geometry() }
