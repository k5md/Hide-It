import tkinter as tk
import i18n

from hide_it.libs.FileInput import FileInput
from hide_it.libs.FileOutput import FileOutput 
from hide_it.utils import load_json, save_json

class ConfigManager(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configs = {}

        # CREATE WIDGETS
        self.config_frame = tk.LabelFrame(self, text = i18n.t("translate.config"), padx = 5, pady = 5)
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

        # PACK WIDGETS
        self.config_file_input.pack(fill = tk.X)
        self.config_file_output.pack(fill = tk.X)
        self.config_frame.pack(fill =  tk.X)

    def add_config(self, entry):
        (key, serializable_manager) = entry
        self.configs[key] = serializable_manager

    def load_config(self, file_path):
        if not file_path:
            return
        try:
            payload = load_json(file_path)
            for key in self.configs:
                serializable_manager = self.configs[key]
                serializable_manager.deserialize(payload[key])
            return file_path
        except Exception as exception:
            return str(exception)
        
    def save_config(self, file_path):
        if not file_path:
            return
        try:
            payload = { key: serializable_manager.serialize() for key, serializable_manager in self.configs.items() }
            save_json(file_path, payload)
            return file_path
        except Exception as exception:
            return str(exception)
