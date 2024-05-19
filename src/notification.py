import tkinter as tk
from PIL import ImageTk, Image

def notify(master, image_path): # Ugly function, will be updated to a class later
    
    def on_click(event):
        print("Window clicked!")
        master.show_page("EditScreenshotPage", image_path = image_path)
        root.destroy()

    def close_window():
        print("Closing window...")
        root.destroy()

    root = tk.Toplevel(master)
    root.title("Image Viewer")
    root.overrideredirect(True)
    
    root.lift()
    root.attributes("-topmost", True)

    # Load your image
    image = Image.open(image_path)

    # Calculate the appropriate size for the window based on the image size
    width, height = image.size
    aspect_ratio = width / height
    new_width = 400  # Set your desired width
    new_height = int(new_width / aspect_ratio)

    # Resize the image to fit the window
    image = image.resize((new_width, new_height))
    tk_image = ImageTk.PhotoImage(image)

    # Create a label to display the image
    label = tk.Label(root, image=tk_image)
    label.pack()

    # Bind the click event to the window
    root.bind("<Button-1>", on_click)
    root.after(5000, close_window)

    root.geometry(f"{new_width+4}x{new_height+4}+50+50")
    
    root.wait_window(root)