import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from functools import partial

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.floater = Overlay(self)

class Overlay(tk.Toplevel):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    MIN_SIZE = (64, 64)

    @staticmethod
    def create_size_grip_image(color, angle):
        image = Image.new('RGBA', (14, 14))
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

    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)

        top_left_resize_grip_image = Overlay.create_size_grip_image("#f00", 180)
        top_right_resize_grip_image = Overlay.create_size_grip_image("#f00", 90)
        bottom_left_resize_grip_image = Overlay.create_size_grip_image("#f00", 270)
        bottom_right_resize_grip_image = Overlay.create_size_grip_image("#f00", 0)

        # CREATE WIDGETS
        self.root_frame = tk.Frame(self)

        self.top_frame = tk.Frame(self.root_frame)
        self.top_left_resize_grip = tk.Label(self.top_frame, image = top_left_resize_grip_image)
        self.close = tk.Label(self.top_frame, text="x")
        self.top_right_resize_grip = tk.Label(self.top_frame, image = top_right_resize_grip_image)

        self.center_frame = tk.Frame(self.root_frame)
        self.position_grip = tk.Label(self.center_frame)

        self.bottom_frame = tk.Frame(self.root_frame)
        self.bottom_left_resize_grip = tk.Label(self.bottom_frame, image = bottom_left_resize_grip_image)
        self.info = tk.Label(self.bottom_frame)
        self.bottom_right_resize_grip = tk.Label(self.bottom_frame, image = bottom_right_resize_grip_image)

        # PACK WIDGETS
        self.top_left_resize_grip.pack(side = tk.LEFT, fill = tk.BOTH)
        self.close.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.top_right_resize_grip.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.top_frame.pack(side = tk.TOP, fill = tk.BOTH)

        self.position_grip.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.center_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.bottom_left_resize_grip.pack(side = tk.LEFT, fill = tk.BOTH)
        self.info.pack(side = tk.LEFT, fill = tk.X, expand = True)
        self.bottom_right_resize_grip.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.bottom_frame.pack(side = tk.BOTTOM, fill = tk.BOTH)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)

        # REGISTER LISTENERS
        self.top_left_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.TOP_LEFT))
        self.top_right_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.TOP_RIGHT))

        self.position_grip.bind("<Button-1>", self.press)
        self.position_grip.bind("<B1-Motion>", self.drag)

        self.bottom_left_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.BOTTOM_LEFT))
        self.bottom_right_resize_grip.bind("<B1-Motion>", partial(self.resize, side = Overlay.BOTTOM_RIGHT))

        # CONFIGURE WIDGETS
        self.top_left_resize_grip.image = top_left_resize_grip_image
        self.top_right_resize_grip.image = top_right_resize_grip_image
        self.bottom_left_resize_grip.image = bottom_left_resize_grip_image
        self.bottom_right_resize_grip.image = bottom_right_resize_grip_image
        
        self.overrideredirect(True)
        self.minsize(*Overlay.MIN_SIZE)
        self.attributes('-topmost', True)
        self.update()

    def press(self, event):
        self.press_x = event.x
        self.press_y = event.y

    def drag(self, event):
        dx = event.x - self.press_x
        dy = event.y - self.press_y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}")

    def resize(self, event, side):
        min_w = self.minsize()[0]
        min_h = self.minsize()[1]
        (x0, y0, x1, y1) = (self.winfo_rootx(), self.winfo_rooty(), self.winfo_pointerx(), self.winfo_pointery())
        # offsets from mouse to window
        dx = x1 - x0 
        dy = y1 - y0
        if side == Overlay.BOTTOM_RIGHT: (x, y, w, h) = (x0, y0, dx, dy)
        if side == Overlay.TOP_LEFT: (x, y, w, h) = (x1, y1, self.winfo_width() - dx, self.winfo_height() - dy)
        if side == Overlay.TOP_RIGHT: (x, y, w, h) = (x1 - dx, y1, dx, self.winfo_height() - dy)
        if side == Overlay.BOTTOM_LEFT: (x, y, w, h) = (x1, y1 - dy, -dx + self.winfo_width(), dy)
        # prevent window from moving
        if (w < min_w): (x, w) = (x0, min_w)
        if (h < min_h): (y, h) = (y0, min_h)
        self.geometry(f"{w}x{h}+{x}+{y}")

app = App()
app.mainloop()
