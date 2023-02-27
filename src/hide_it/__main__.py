import tkinter as tk
import itertools

from hide_it.Overlay import Overlay

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.settings = {
            "overlays": [],
            "toggle_overlays_key": '.'
        }
        self.overlays = {}
        self.overlays_key_generator = itertools.count()
        
        # CREATE WIDGETS
        self.root_frame = tk.Frame(self)

        self.add_overlay_label = tk.Label(self.root_frame, text = "+")

        # PACK WIDGETS
        self.add_overlay_label.pack()
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # REGISTER LISTENERS
        self.add_overlay_label.bind("<Button-1>", lambda event: self.add_overlay())

    def add_overlay(self, settings = {}):
        key = next(self.overlays_key_generator)
        def overlay_close_handler(event):
            if key not in self.overlays:
                return
            self.overlays[key].destroy()
            del self.overlays[key]
        overlay = Overlay(self, **settings, overlay_close_handler = overlay_close_handler)
        self.overlays[key] = overlay 

app = App()
app.mainloop()
