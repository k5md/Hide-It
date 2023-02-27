import os
import sys
import tkinter as tk
import itertools
import i18n
import locale

from hide_it.libs.FileInput import FileInput
from hide_it.libs.FileOutput import FileOutput 
from hide_it.Overlay import Overlay
from hide_it.utils import load_json, save_json

locale.setlocale(locale.LC_ALL, "")

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    approot = os.path.dirname(sys.executable)

LOCALES_PATH = os.path.join(approot, "locales")

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        i18n.load_path.append(LOCALES_PATH)
        i18n.set("fallback", "en")
        i18n.set("locale", locale.getlocale()[0][0:2].lower())

        self.overlays = {}
        self.overlays_key_generator = itertools.count()
        
        # CREATE WIDGETS
        self.root_frame = tk.Frame(self, padx = 5, pady = 5)

        self.config_frame = tk.LabelFrame(self.root_frame, text = i18n.t("translate.config"), padx = 5, pady = 5)
        self.config_file_input = FileInput(self.config_frame, file_input_handler = self.load_config, file_input_title = i18n.t("translate.load"), pady = 5)
        self.config_file_output = FileOutput(self.config_frame, file_output_handler = self.save_config, file_output_title= i18n.t("translate.save"))

        self.overlays_controls_frame = tk.LabelFrame(self.root_frame, text = i18n.t("translate.actions"), padx = 5, pady = 5)
        self.add_overlay_label = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.addOverlay"), command = self.add_overlay)

        # PACK WIDGETS
        self.config_file_input.pack(fill = tk.X)
        self.config_file_output.pack(fill = tk.X)
        self.config_frame.pack(fill =  tk.X)

        self.add_overlay_label.pack(fill = tk.X)
        self.overlays_controls_frame.pack(fill = tk.BOTH, expand = True)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # CONFIGURE WIDGETS
        self.geometry("300x200")
        self.minsize(300, 200)
        self.maxsize(300, 200)
        self.attributes("-topmost", True)

    def add_overlay(self, config = {}):
        key = next(self.overlays_key_generator)
        overlay = Overlay(self, **config, overlay_close_handler = lambda event: self.remove_overlay(key))
        self.overlays[key] = overlay
    
    def remove_overlay(self, key):
        if key not in self.overlays:
            return
        self.overlays[key].destroy()
        del self.overlays[key]
    
    def remove_overlays(self):
        for key in list(self.overlays.keys()):
            self.remove_overlay(key)

    def load_config(self, file_path):
        try:
            payload = load_json(file_path)
            self.remove_overlays()
            for config in payload["overlays"]: self.add_overlay(config)
            return file_path
        except Exception as exception:
            return str(exception)
        
    def save_config(self, file_path):
        try:
            payload = {
                "overlays": [ overlay.serialize() for overlay in self.overlays.values() ],
            }
            save_json(file_path, payload)
            return False
        except Exception as exception:
            return str(exception)

app = App()
app.mainloop()
