import tkinter as tk

from hide_it.utils import enable_clickthrough, disable_clickthrough

class OverlayWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        # CONFIGURE WIDGETS
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        
    def lock(self):
        enable_clickthrough(self.winfo_id())
        self.attributes("-transparentcolor", self.overlay_color)
        self.attributes("-topmost", True)

    def unlock(self):
        disable_clickthrough(self.winfo_id())
        self.attributes("-transparentcolor", "")
        self.attributes("-topmost", True)
