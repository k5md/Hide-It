import tkinter as tk
import re
from functools import partial
import i18n

from hide_it.utils import apply_to_widget_and_children, find_matching_color, make_draggable, make_resizable
from hide_it.libs.ResizeGrip import ResizeGrip
from hide_it.libs.OverlayWindow import OverlayWindow

class Overlay(OverlayWindow):
    @staticmethod
    def change_background_color(widget, color, highlight_color):
        if type(widget) is ResizeGrip:
            widget.config(background = color)
        if type(widget) is tk.Frame:
            widget.config(background = color)
        if type(widget) is tk.Label:
            widget.config(background = color)
        if type(widget) is Overlay:
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

    def __init__(self, *args, overlay_color = "#000", overlay_geometry = "0x0+0+0", overlay_opacity = "1", overlay_close_handler = lambda event: None, **kwargs):
        super().__init__(*args, **kwargs)

        self.overlay_color = overlay_color
        self.overlay_color_string_var = tk.StringVar(value = self.overlay_color)

        self.overlay_opacity = overlay_opacity
        self.overlay_opacity_string_var = tk.StringVar(value = self.overlay_opacity)

        # CREATE WIDGETS
        self.root_frame = tk.Frame(self)

        self.top_frame = tk.Frame(self.root_frame)
        self.top_left_resize_grip = ResizeGrip(self.top_frame, resize_grip_angle = 180)
        self.close_label = tk.Label(self.top_frame, text="x")
        self.top_right_resize_grip = ResizeGrip(self.top_frame, resize_grip_angle = 90)

        self.center_frame = tk.Frame(self.root_frame)
        self.position_grip = tk.Label(self.center_frame, text = i18n.t("translate.dragOverlay"))

        self.bottom_frame = tk.Frame(self.root_frame)
        self.bottom_left_resize_grip = ResizeGrip(self.bottom_frame, resize_grip_angle = 270)
        self.overlay_color_frame = tk.Frame(self.bottom_frame)
        self.overlay_color_label = tk.Label(self.overlay_color_frame, text = "{}:".format(i18n.t("translate.color")))
        self.overlay_color_entry = tk.Entry(self.overlay_color_frame, textvariable = self.overlay_color_string_var, width = 8, justify = tk.CENTER, bd = 0, highlightthickness = 0)
        self.overlay_opacity_frame = tk.Frame(self.bottom_frame)
        self.overlay_opacity_label = tk.Label(self.overlay_opacity_frame, text = "{}:".format(i18n.t("translate.opacity")))
        self.overlay_opacity_entry = tk.Entry(self.overlay_opacity_frame, textvariable = self.overlay_opacity_string_var, width = 8, justify = tk.CENTER, bd = 0, highlightthickness = 0)
        self.bottom_right_resize_grip = ResizeGrip(self.bottom_frame, resize_grip_angle = 0)

        # PACK WIDGETS
        self.top_left_resize_grip.pack(side = tk.LEFT, fill = tk.BOTH)
        self.close_label.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.top_right_resize_grip.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.top_frame.pack(side = tk.TOP, fill = tk.BOTH)

        self.position_grip.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.center_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.bottom_left_resize_grip.pack(side = tk.LEFT, fill = tk.BOTH)
        self.overlay_color_frame.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.overlay_color_entry.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.overlay_color_label.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.bottom_right_resize_grip.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.overlay_opacity_frame.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)
        self.overlay_opacity_label.pack(side = tk.LEFT, fill = tk.BOTH)
        self.overlay_opacity_entry.pack(side = tk.LEFT, fill = tk.BOTH)
        self.bottom_frame.pack(side = tk.BOTTOM, fill = tk.BOTH)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # REGISTER LISTENERS
        make_resizable(self, self.top_left_resize_grip, tk.NW)
        self.close_label.bind("<Button-1>", overlay_close_handler)
        make_resizable(self, self.top_right_resize_grip, tk.NE)

        make_draggable(self, self.position_grip)

        make_resizable(self, self.bottom_left_resize_grip, tk.SW)
        self.overlay_color_string_var.trace_add("write", lambda *args, **kwargs: self.handle_color())
        self.overlay_opacity_string_var.trace_add("write", lambda *args, **kwargs: self.handle_opacity())
        make_resizable(self, self.bottom_right_resize_grip, tk.SE)

        # CONFIGURE WIDGETS       
        (wh, x, y) = overlay_geometry.split("+")
        (w, h) = wh.split("x")
        if (int(w) > 0 and int(h) > 0):
            self.geometry(overlay_geometry)
        self.handle_color()
        self.handle_opacity()
        self.update()

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
    
    def handle_opacity(self):
        opacity = self.overlay_opacity_string_var.get()
        opacity_valid = re.search(r'^\d(\.\d{0,2})?$', opacity)
        if not opacity_valid:
            return
        self.overlay_opacity = opacity
        self.attributes("-alpha", float(opacity))

    def lock(self):
        super().lock()
        self.root_frame.pack_forget()

    def unlock(self):
        super().unlock()
        self.root_frame.pack(fill = tk.BOTH, expand = True)

    def serialize(self):
        return { "overlay_color": self.overlay_color, "overlay_opacity": self.overlay_opacity, "overlay_geometry": self.winfo_geometry() }
