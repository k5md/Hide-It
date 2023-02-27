import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class ResizeGrip(tk.Label):
    @staticmethod
    def create_resize_grip_image(color, angle):
        image = Image.new("RGBA", (14, 14))
        draw = ImageDraw.Draw(image)
        coords = [
            (9, 3, 10, 4),
            (6, 6, 7, 7),
            (9, 6, 10, 7),
            (3, 9, 4, 10),
            (6, 9, 7, 10),
            (9, 9, 10, 10),
        ]
        for coord in coords:
            draw.rectangle(coord, fill = color)
        image = image.rotate(angle)
        return ImageTk.PhotoImage(image)

    def __init__(self, *args, resize_grip_color = "#000", resize_grip_angle = 0, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        self.resize_grip_color = resize_grip_color
        self.resize_grip_angle = resize_grip_angle
        self.update_resize_grip()
    
    def update_resize_grip(self):
        resize_grip_image = ResizeGrip.create_resize_grip_image(self.resize_grip_color, self.resize_grip_angle)
        self.configure(image = resize_grip_image)
        self.image = resize_grip_image
    
    def change_resize_grip_color(self, color):
        self.resize_grip_color = color
        self.update_resize_grip()

    def change_resize_grip_angle(self, angle):
        self.resize_grip_angle = angle
        self.update_resize_grip()