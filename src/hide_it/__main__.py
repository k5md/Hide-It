import os
import sys
import tkinter as tk
import i18n
import locale

from hide_it.OverlaysManager import OverlaysManager
from hide_it.ConfigManager import ConfigManager

locale.setlocale(locale.LC_ALL, "")

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    approot = os.path.dirname(sys.executable)

LOCALES_PATH = os.path.join(approot, "locales")
ICON_PATH = os.path.join(approot, "assets", "hide_it.ico")

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        i18n.load_path.append(LOCALES_PATH)
        i18n.set("fallback", "en")
        i18n.set("locale", locale.getlocale()[0][0:2].lower())

        # CREATE WIDGETS
        self.root_frame = tk.Frame(self, padx = 5, pady = 5)

        self.config_manager_frame = ConfigManager(self.root_frame)
        self.overlays_manager_frame = OverlaysManager(self.root_frame)

        # PACK WIDGETS
        self.config_manager_frame.pack(fill = tk.X)
        self.overlays_manager_frame.pack(fill = tk.BOTH, expand = True)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # CONFIGURE WIDGETS
        self.config_manager_frame.add_config(("overlays", self.overlays_manager_frame))

        self.title(i18n.t("translate.appTitle"))
        self.iconbitmap(ICON_PATH)

app = App()
app.mainloop()
