import tkinter as tk
import tkinter.filedialog

class FileOutput(tk.Frame):
    def __init__(self, *args, file_output_handler, file_output_title, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.file_output_handler = file_output_handler
        self.picked_file_path_string_var = tk.StringVar()

        # CREATE WIDGETS
        self.root_frame = tk.Frame(self)

        self.pick_file_button = tk.Button(self.root_frame, text = file_output_title, command = self.handle_pick)
        self.picked_file_path_entry = tk.Entry(self.root_frame, textvariable = self.picked_file_path_string_var, state = tk.DISABLED)

        # PACK WIDGETS
        self.pick_file_button.pack(side = tk.LEFT, fill = tk.BOTH, expand = False)
        self.picked_file_path_entry.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)
        
        self.root_frame.pack(fill = tk.BOTH, expand = True)
    
    def handle_pick(self):
        file_path = tk.filedialog.asksaveasfilename()
        result = self.file_output_handler(file_path)
        if not result:
            return
        self.picked_file_path_string_var.set(result)
