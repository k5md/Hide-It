import tkinter as tk
import itertools
import i18n

from hide_it.Overlay import Overlay

class OverlaysManager(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.overlays = {}
        self.overlays_editable = True
        self.overlays_visible = True
        self.overlays_key_generator = itertools.count()

        # CREATE WIDGETS
        self.overlays_controls_frame = tk.LabelFrame(self, text = i18n.t("translate.actions"), padx = 5, pady = 5)
        self.add_overlay_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.addOverlay"), command = self.add_overlay)
        self.toggle_overlays_visible_button = tk.Button(self.overlays_controls_frame)
        self.toggle_overlays_editable_button = tk.Button(self.overlays_controls_frame)
        self.close_overlays_button = tk.Button(self.overlays_controls_frame, text = i18n.t("translate.removeOverlays"), command = self.remove_overlays)

        # PACK WIDGETS
        self.add_overlay_button.pack(fill = tk.X)
        self.toggle_overlays_visible_button.pack(fill = tk.X)
        self.toggle_overlays_editable_button.pack(fill = tk.X)
        self.close_overlays_button.pack(fill = tk.X)
        self.overlays_controls_frame.pack(fill = tk.BOTH, expand = True)

        # CONFIGURE WIDGETS
        self.update()

    def add_overlay(self, config = {}):
        key = next(self.overlays_key_generator)
        overlay = Overlay(self, **config, overlay_close_handler = lambda event: self.remove_overlay(key))
        overlay.title(i18n.t("translate.overlayTitle", id = key))
        self.overlays[key] = overlay
        self.update()
    
    def remove_overlay(self, key):
        if key not in self.overlays:
            return
        self.overlays[key].destroy()
        del self.overlays[key]
        self.update()
    
    def remove_overlays(self):
        for key in list(self.overlays.keys()):
            self.remove_overlay(key)
        self.update()
    
    def lock_overlays(self):
        for overlay in self.overlays.values(): overlay.lock()
        self.overlays_editable = False
        self.update()

    def unlock_overlays(self):
        for overlay in self.overlays.values(): overlay.unlock()
        self.overlays_editable = True
        self.update()
    
    def hide_overlays(self):
        for overlay in self.overlays.values(): overlay.withdraw()
        self.overlays_visible = False
        self.update()
    
    def show_overlays(self):
        for overlay in self.overlays.values(): overlay.deiconify()
        self.overlays_visible = True
        self.update()
    
    def update(self):
        if self.overlays_visible: visible = { "text": i18n.t("translate.hideOverlays"), "command": self.hide_overlays }
        else: visible = { "text": i18n.t("translate.showOverlays"), "command": self.show_overlays }
        visible["state"] = tk.NORMAL if bool(self.overlays) else tk.DISABLED
        self.toggle_overlays_visible_button.config(**visible)

        if self.overlays_editable: editable = { "text":  i18n.t("translate.lockOverlays"), "command": self.lock_overlays }
        else: editable = { "text": i18n.t("translate.unlockOverlays"), "command": self.unlock_overlays }
        editable["state"] = tk.NORMAL if bool(self.overlays) else tk.DISABLED
        self.toggle_overlays_editable_button.config(**editable)

        closable = bool(self.overlays)
        self.close_overlays_button.config(state = tk.NORMAL if closable else tk.DISABLED)

        super().update()

    def serialize(self):
        return [ overlay.serialize() for overlay in self.overlays.values() ]

    def deserialize(self, payload):
        self.remove_overlays()
        for config in payload:
            self.add_overlay(config)
