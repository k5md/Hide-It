import tkinter as tk
import tkinter.ttk

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.floater = FloatingWindow(self)

class FloatingWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.overrideredirect(True)

        self.label = tk.Label(self, text="Click on the grip to move")
        self.grip = tk.Label(self, bitmap="gray25")
        self.size_grip = tk.ttk.Sizegrip(self)
        self.grip.pack(side="left", fill="y")
        self.label.pack(side="right", fill="both", expand=True)
        self.size_grip.pack(side="right", fill="y")
        self.size_grip.lift()

        self.grip.bind("<ButtonPress-1>", self.start_move)
        self.grip.bind("<ButtonRelease-1>", self.stop_move)
        self.grip.bind("<B1-Motion>", self.do_move)

        self.size_grip.bind("<B1-Motion>", self.resize_move)

        self.label.configure(background="black")
        self.attributes('-topmost',True)
        
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def resize_move(self, event):
        x1 = self.winfo_pointerx()
        y1 = self.winfo_pointery()
        x0 = self.winfo_rootx()
        y0 = self.winfo_rooty()
        x = x1 - x0
        y = y1 - y0
        self.geometry(f"{x}x{y}")
        return

app=App()
app.mainloop()

