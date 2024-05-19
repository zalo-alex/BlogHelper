import time
from src.keyboard_handler import KeyboardHandler

import tkinter as tk
from tkinter import ttk
import sv_ttk
from PIL import ImageTk, Image, ImageDraw

import keyboard

class Window(tk.Tk):
    
    VERSION = ""
    
    def __init__(self, version):
        tk.Tk.__init__(self)
        
        Window.VERSION = version
        
        self.title("Blog Helper")
        
        KeyboardHandler.init(self)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)

        self.pages = {
            "StartPage": StartPage,
            "EditScreenshotPage": EditScreenshotPage,
            "EditTextNotePage": EditTextNotePage
        }
        
        self.current_frame = None

        self.show_page("StartPage")
        
        sv_ttk.set_theme("light")

    def show_page(self, cont, **kwargs):
        
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = self.pages[cont](self.container, self, **kwargs)
        self.current_frame.grid(row=0, column=0, sticky="ew", columnspan=2)

    @staticmethod
    def run(version):
        window = Window(version)
        window.mainloop()
        return window

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.title = tk.Label(self, text="Blog Helper", font=("Helvetica", 24), justify="center")
        self.title.pack(expand=True, fill="x", pady=10, padx=50)
        
        frame = tk.Frame(self)
        frame.pack(pady=10)

        label = tk.Label(frame, text="Screenshot: ", font=("Helvetica", 12, "bold"))
        label.pack(side="left")

        self.screenshot_hotkey_label = tk.Label(frame, text=KeyboardHandler.HOTKEYS["screenshot"]["hotkey"], font=("Consolas", 12) ,fg='green', padx=4)
        self.screenshot_hotkey_label.pack(side="left")

        button = ttk.Button(frame, text="✏", command=lambda: self.change_hotkey("screenshot"))
        button.pack(side="left")

        frame = tk.Frame(self)
        frame.pack(pady=10)

        label = tk.Label(frame, text="Text note: ", font=("Helvetica", 12, "bold"))
        label.pack(side="left")

        self.text_note_hotkey_label = tk.Label(frame, text=KeyboardHandler.HOTKEYS["text_note"]["hotkey"], font=("Consolas", 12) ,fg='green', padx=4)
        self.text_note_hotkey_label.pack(side="left")

        button = ttk.Button(frame, text="✏", command=lambda: self.change_hotkey("text_note"))
        button.pack(side="left")
        
        ttk.Label(self, text=f"Alex ZALO © 2024 | v{Window.VERSION}", font=("Consolas", 8)).pack(pady=10)
        
        self.hotkey_labels = {
            "screenshot": self.screenshot_hotkey_label,
            "text_note": self.text_note_hotkey_label
        }
        
        self.controller.geometry('')
    
    def change_hotkey(self, name):
        hotkey = keyboard.read_hotkey()
        KeyboardHandler.set_hotkey(name, hotkey)
        self.hotkey_labels[name].config(text=hotkey)
        keyboard.stash_state()


class EditScreenshotPage(tk.Frame):
    def __init__(self, parent, controller, image_path):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.mouse_down = False
        self.mouse_down_pos = (0, 0)
        
        self.rect = False

        ## Tk

        self.label = tk.Label(self)
        self.label.pack()
        
        self.label.bind("<ButtonPress-1>", self.on_mouse_down)
        self.label.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.label.bind("<B1-Motion>", self.on_mouse_move)

        button = ttk.Button(self, text="🏠", command=self.back)
        button.pack(side="left", pady=5, padx=5)
        
        self.rect_button = ttk.Button(self, text="⬜", command=self.toggle_rect)
        self.rect_button.pack(side="left", pady=5, padx=5)
        
        self.save_button = ttk.Button(self, text="💾", command=self.save_file)
        self.save_button.pack(side="left", pady=5, padx=5)
        
        self.save__and_exit_button = ttk.Button(self, text="✔", command=self.save_and_exit)
        self.save__and_exit_button.pack(side="left", pady=5, padx=5)
        
        ## Image Canvas
        
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()
        self.draw = ImageDraw.Draw(self.image)
        
        self.update_image()
        
        self.controller.geometry(f"{int(self.image.size[0] / 2)}x{int(self.image.size[1] / 2) + 45}")
        
        ## On Top
        
        self.controller.lift()
        self.controller.attributes("-topmost", True)
        self.controller.deiconify()
        self.controller.after_idle(self.controller.attributes, '-topmost', False)
    
    def save_file(self):
        filename = f"output/{int(time.time())}.png"
        self.last_image.save(filename)
        self.save_button.config(text="✅")
    
    def save_and_exit(self):
        self.save_file()
        
        self.controller.attributes("-topmost", False)
        self.controller.lower()
        
        self.back()
    
    def toggle_rect(self):
        if self.rect:
            self.rect_button.config(text="⬜")
        else:
            self.rect_button.config(text="⬛")
        self.rect = not self.rect
    
    def on_mouse_down(self, event):
        if self.rect:
            self.mouse_down = True
            self.mouse_down_pos = self.get_relative_position(event)
            self.update_relative_position(event)

    def on_mouse_up(self, event):
        self.mouse_down = False

    def on_mouse_move(self, event):
        if self.mouse_down:
            self.update_relative_position(event)
    
    def get_relative_position(self, event):
        label_x, label_y = self.label.winfo_rootx(), self.label.winfo_rooty()
        mouse_x, mouse_y = event.x_root, event.y_root
        relative_x = mouse_x - label_x
        relative_y = mouse_y - label_y
        return relative_x * 2, relative_y * 2

    def update_relative_position(self, event):
        relative_x, relative_y = self.get_relative_position(event)
        self.draw.rectangle([self.mouse_down_pos, (relative_x, relative_y)], outline="red", width=4)
        self.update_image()
    
    def back(self):
        self.label.config(image="")
        self.controller.show_page("StartPage")
    
    def update_image(self):
        self.tk_image = self.get_tk_image()
        self.last_image = self.image.copy()
        self.image = self.original_image.copy()
        self.draw = ImageDraw.Draw(self.image)
        
        self.label.config(image=self.tk_image)
        
        self.save_button.config(text="💾")
    
    def get_tk_image(self):
        return ImageTk.PhotoImage(self.image.resize((int(self.image.size[0] / 2), int(self.image.size[1] / 2))))
        
class EditTextNotePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ## Tk
        
        self.text = tk.Text(self, width=64, height=20)
        self.text.pack()

        button = ttk.Button(self, text="🏠", command=self.back)
        button.pack(side="left", pady=5, padx=5)
        
        self.save_button = ttk.Button(self, text="💾", command=self.save_file)
        self.save_button.pack(side="left", pady=5, padx=5)
        
        self.save__and_exit_button = ttk.Button(self, text="✔", command=self.save_and_exit)
        self.save__and_exit_button.pack(side="left", pady=5, padx=5)
        
        ## On Top
        
        self.controller.lift()
        self.controller.attributes("-topmost", True)
        self.controller.deiconify()
        self.controller.after_idle(self.controller.attributes, '-topmost', False)
    
    def save_file(self):
        filename = f"output/{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(self.text.get("1.0", tk.END))
        self.save_button.config(text="✅")
    
    def save_and_exit(self):
        self.save_file()
        
        self.controller.attributes("-topmost", False)
        self.controller.lower()
        
        self.back()
    
    def back(self):
        self.controller.show_page("StartPage")