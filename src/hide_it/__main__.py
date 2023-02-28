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
        self.config_file_input = FileInput(
            self.config_frame,
            file_input_handler = self.load_config,
            file_input_title = i18n.t("translate.load"),
            file_input_dialog_props = { "filetypes": [("JSON",".json"), (i18n.t("translate.allTypes"), "*.*")] },
            pady = 5,
        )
        self.config_file_output = FileOutput(
            self.config_frame,
            file_output_handler = self.save_config,
            file_output_title = i18n.t("translate.save"),
            file_output_dialog_props = { "filetypes": [("JSON",".json")], "defaultextension": ".json" },
        )

        self.overlays_controls_frame = tk.LabelFrame(self.root_frame, text = i18n.t("translate.actions"), padx = 5, pady = 5)
        self.add_overlay_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.addOverlay"), command = self.add_overlay)
        self.lock_overlays_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.lockOverlays"), command = self.lock_overlays)
        self.unlock_overlays_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.unlockOverlays"), command = self.unlock_overlays)

        # PACK WIDGETS
        self.config_file_input.pack(fill = tk.X)
        self.config_file_output.pack(fill = tk.X)
        self.config_frame.pack(fill =  tk.X)

        self.add_overlay_button.pack(fill = tk.X)
        self.overlays_controls_frame.pack(fill = tk.BOTH, expand = True)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # CONFIGURE WIDGETS
        self.geometry("360x200")
        self.minsize(360, 200)
        self.maxsize(360, 200)
        self.attributes("-topmost", True)

        self.unlock_overlays()

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
    
    def lock_overlays(self):
        self.lock_overlays_button.pack_forget()
        self.unlock_overlays_button.pack(fill = tk.X)
        for overlay in self.overlays.values(): overlay.lock()

    def unlock_overlays(self):
        self.unlock_overlays_button.pack_forget()
        self.lock_overlays_button.pack(fill = tk.X)
        for overlay in self.overlays.values(): overlay.unlock()
    
    def load_config(self, file_path):
        if not file_path:
            return
        try:
            payload = load_json(file_path)
            self.remove_overlays()
            for config in payload["overlays"]: self.add_overlay(config)
            return file_path
        except Exception as exception:
            return str(exception)
        
    def save_config(self, file_path):
        if not file_path:
            return
        try:
            payload = {
                "overlays": [ overlay.serialize() for overlay in self.overlays.values() ],
            }
            save_json(file_path, payload)
            return file_path
        except Exception as exception:
            return str(exception)

app = App()
app.mainloop()
