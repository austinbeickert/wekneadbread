import tkinter as tk
import json
from tkinter import *
from PIL import Image, ImageTk

root = tk.Tk()
root.title("We Knead Bread")
root.geometry("1920x1080")
root.resizable(True, False)
root.config(background="DarkOrange4")

#main container
main_frame = tk.Frame(root, bg="DarkOrange4")
main_frame.pack(fill="both", expand=True)

#left column
gray_baker_frame = tk.Frame(main_frame, width=640, bg="DarkOrange1")
gray_baker_frame.pack(side=tk.LEFT, fill="y", padx=(10, 0), pady=10)
gray_baker_frame.pack_propagate(False)

#left column containers
    #title
gray_baker_top_frame = tk.Frame(gray_baker_frame, width=620, height=50, bg="gray")
gray_baker_top_frame.pack(padx=10, pady=5)
tk.Label(gray_baker_top_frame, text="Head Chef", bg="gray").pack(padx=10, pady=10)
gray_baker_top_frame.pack_propagate(False)
    #click button
gray_baker_click_frame = tk.Frame(gray_baker_frame, width=620, height=350, bg="gray")
gray_baker_click_frame.pack(padx=10, pady=5)
tk.Label(gray_baker_click_frame, text="Click for bread", bg="gray").pack(padx=10, pady=10)
gray_baker_click_frame.pack_propagate(False)
    #upgrades
gray_baker_upgrade_frame = tk.Frame(gray_baker_frame, width=620, height=620, bg="gray")
gray_baker_upgrade_frame.pack(padx=10, pady=10)
tk.Label(gray_baker_upgrade_frame, text="Upgrades here", bg="gray").pack(padx=10, pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

#main bake paw button
cat_pil = Image.open("catpaw3.png").convert("RGBA")
cat_image = ImageTk.PhotoImage(cat_pil)
click_paw = tk.Button(gray_baker_click_frame, image=cat_image)
click_paw.image = cat_image
click_paw.pack(pady=10)

#right column containers
stray_baker_frame = tk.Frame(main_frame, width=640, bg="DarkOrange1")
stray_baker_frame.pack(side=tk.RIGHT, fill="y", padx=(0,10), pady=10)
stray_baker_frame.pack_propagate(False)
    #title
stray_baker_top_frame = tk.Frame(stray_baker_frame, width=620, height=50, bg="gray")
stray_baker_top_frame.pack(padx=10, pady=5)
tk.Label(stray_baker_top_frame, text="Stray Bakers", bg="gray").pack(padx=10, pady=10)
stray_baker_top_frame.pack_propagate(False)
    #image of strays
stray_baker_image_frame = tk.Frame(stray_baker_frame, width=620, height=290, bg="gray")
stray_baker_image_frame.pack(padx=10, pady=5)
tk.Label(stray_baker_image_frame, text="Stray baker image", bg="gray").pack(padx=10,pady=10)
stray_baker_image_frame.pack_propagate(False)
    #energy level
stray_baker_energy_frame = tk.Frame(stray_baker_frame, width=620, height=50, bg="gray")
stray_baker_energy_frame.pack(padx=10, pady=5)
tk.Label(stray_baker_energy_frame, text="Stray Baker Energy", bg="gray").pack(padx=10, pady=10)
stray_baker_energy_frame.pack_propagate(False)
    #upgrades
stray_baker_upgrade_frame = tk.Frame(stray_baker_frame, width=620, height=620, bg="gray")
stray_baker_upgrade_frame.pack(padx=10, pady=10)
tk.Label(stray_baker_upgrade_frame, text="Upgrades here", bg="gray").pack(padx=10, pady=10)
stray_baker_upgrade_frame.pack_propagate(False)

#middle column
middle_frame = tk.Frame(main_frame, bg="DarkOrange4")
middle_frame.pack(padx=10, pady=10)

#top middle box
bread_count_frame = tk.Frame(middle_frame, width=640, height=400, bg="DarkOrange1")
bread_count_frame.pack(pady=(0,0))
tk.Label(bread_count_frame, text="Bread Count", bg="DarkOrange1").pack(padx=10, pady=10)
bread_count_frame.pack_propagate(False)

#bottom middle box
gumbie_frame = tk.Frame(middle_frame, width=640, height=660, bg="DarkOrange1")
gumbie_frame.pack(pady=(10,0))
    #gumbie upgrades
gumbie_upgrade_frame = tk.Frame(gumbie_frame, width=620, height=220, bg="gray")
gumbie_upgrade_frame.pack(padx=10, pady=(10,0))
tk.Label(gumbie_upgrade_frame, text="Upgrades here", bg="gray").pack(padx=10, pady=10)
gumbie_upgrade_frame.pack_propagate(False)
    #feed gumbie button
feed_gumbie_frame = tk.Frame(gumbie_frame, width=620, height=620, bg="gray")
feed_gumbie_frame.pack(padx=10, pady=10)
tk.Label(feed_gumbie_frame, text="Feed gumbie", bg="gray").pack(padx=10, pady=10)
feed_gumbie_frame.pack_propagate(False)

root.mainloop()

