import tkinter as tk
from tkinter import Toplevel, Label
from PIL import Image, ImageTk
import subprocess

def open_space1():
    subprocess.run(["python", "space1.py"])

def open_space2():
    subprocess.run(["python", "space2.py"])

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(image)

# Create the main window
root = tk.Tk()
root.title("Image Project")

# Set the fixed size for images
fixed_width = 600
fixed_height = 400

# Create the main container
frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

# Add image1
image1 = resize_image("car4.jpg", fixed_width, fixed_height)
image1_label = tk.Label(frame, image=image1)
image1_label.grid(row=0, column=0, padx=10, pady=10)

# Add button1
button1 = tk.Button(frame, text="Picture 1", command=open_space1)
button1.grid(row=1, column=0, padx=10, pady=10)

# Add image2
image2 = resize_image("car6.jpg", fixed_width, fixed_height)
image2_label = tk.Label(frame, image=image2)
image2_label.grid(row=0, column=1, padx=10, pady=10)

# Add button2
button2 = tk.Button(frame, text="Picture 2", command=open_space2)
button2.grid(row=1, column=1, padx=10, pady=10)

# Start the main loop
root.mainloop()
