import tkinter as tk
import itertools
import i18n

from hide_it.Overlay import Overlay

class OverlaysManager(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.overlays = {}
        self.overlays_key_generator = itertools.count()

        # CREATE WIDGETS
        self.overlays_controls_frame = tk.LabelFrame(self, text = i18n.t("translate.actions"), padx = 5, pady = 5)
        self.add_overlay_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.addOverlay"), command = self.add_overlay)
        self.lock_overlays_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.lockOverlays"), command = self.lock_overlays)
        self.unlock_overlays_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.unlockOverlays"), command = self.unlock_overlays)

        # PACK WIDGETS
        self.add_overlay_button.pack(fill = tk.X)
        self.overlays_controls_frame.pack(fill = tk.BOTH, expand = True)

        # CONFIGURE WIDGETS
        self.unlock_overlays()

    def add_overlay(self, config = {}):
        key = next(self.overlays_key_generator)
        overlay = Overlay(self, **config, overlay_close_handler = lambda event: self.remove_overlay(key))
        overlay.title(i18n.t("translate.overlayTitle", id = key))
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
    
    def serialize(self):
        return [ overlay.serialize() for overlay in self.overlays.values() ]

    def deserialize(self, payload):
        self.remove_overlays()
        for config in payload:
            self.add_overlay(config)
