import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import random

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'

def get_random_nasa_image():
    url = "https://images-api.nasa.gov/search?q=space&media_type=image"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    try:
        items = data['collection']['items']
        random_item = random.choice(items)  # Choose a random item from the list
        image_url = random_item['links'][0]['href']
        description = random_item['data'][0]['description']
        return image_url, description
    except KeyError as e:
        print("Error:", e)
        print("Response:", data)
        return None, None

def show_random_nasa_image():
    image_url, description = get_random_nasa_image()
    if image_url and description:
        image_response = requests.get(image_url)
        image_data = Image.open(BytesIO(image_response.content))
        image_data.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image_data)
        canvas.image = photo  # Keep a reference to prevent garbage collection
        canvas.delete("image")  # Clear previous image
        canvas.create_image(root.winfo_width()/2, root.winfo_height()/3, anchor=tk.CENTER, image=photo, tag="image")  # Center image
        # Adjust text font size based on text length
        font_size = 14 if len(description) <= 200 else 12  # Adjust font size threshold as needed
        description_label.config(text=description, font=("Consolas", font_size))
    else:
        description_label.config(text="Failed to fetch image.")

def on_resize(event):
    bg_image_resized = bg_image.resize((event.width, event.height), Image.LANCZOS)
    bg_photo_resized = ImageTk.PhotoImage(bg_image_resized)
    canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo_resized)
    canvas.image = bg_photo_resized  # Keep a reference to prevent garbage collection

# Create main window
root = tk.Tk()
root.title("NASA Image Viewer")
root.geometry("800x700")  # Adjust window size here
root.minsize(400, 400)  # Set minimum size to ensure the button is visible

# Load background image
bg_image = Image.open("cosmos_background.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas for background
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.bind("<Configure>", on_resize)

# Add background image to canvas
canvas.create_image(0, 0, anchor=tk.NW, image=bg_photo)

# Create description label
description_label = ttk.Label(root, wraplength=600, justify="center")
description_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Create button to show a random NASA image
show_image_button = ttk.Button(root, text="Show me a picture", command=show_random_nasa_image)
show_image_button.pack(side="bottom")

# Run the application
root.mainloop()
