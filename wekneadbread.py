import tkinter as tk
import json
from tkinter import PhotoImage
from PIL import Image, ImageTk

#Debug switch
debug = True

#Initialize game state by reading lines in "savedata.txt" created through save_game_state() 
def load_game_state():
     global bread_count, stray_bakers, upgrade_cost, num_baked_stray, num_baked_gray
     with open("savedata.txt", "r") as f:
          lines = f.readlines()

          bread_count = float(lines[0])
          num_baked_gray = float(lines[1])
          stray_bakers = float(lines[2])
          num_baked_stray = float(lines[3])
          upgrade_cost = float(lines[4])

load_game_state()

#Set window background and buttons

#window node
root = tk.Tk()
root.title("We Knead Bread")
root.geometry("600x400")
root.resizable(False, False)

#image variables
bg_image = PhotoImage(file="bread3.png")
cat_pil = Image.open("catpaw3.png").convert("RGBA")
cat_image = ImageTk.PhotoImage(cat_pil)

#background image node
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.lower()

#bread counter node
counter_label = tk.Label(root, text="Bread: 0", font=("Ariel", 18))
counter_label.pack(pady=20)


def bake_bread():
    global bread_count, num_baked_gray
    bread_count += 1
    num_baked_gray += 1
    #counter_label.config(text=f"Bread: {bread_count}") #replaced by update_ui() across the board
    update_ui()

#main bake paw button
click_paw = tk.Button(root, image=cat_image, command=bake_bread, borderwidth=0, highlightthickness=0)
click_paw.image = cat_image
click_paw.pack(pady=10)

if debug:
    print("We Knead Bread Initialized")


def hire_stray():
    global bread_count
    global stray_bakers, upgrade_cost
        
    if bread_count >= upgrade_cost:
        bread_count -= upgrade_cost
        stray_bakers += 1
        upgrade_cost = int((upgrade_cost + (upgrade_cost * .15)))
        #counter_label.config(text=f"Bread: {bread_count}")
        #upgrade_button.config(text=f"Hire Stray Baker ({stray_bakers}) - Cost: {upgrade_cost}",)
    update_ui()

#hire stray button
upgrade_button = tk.Button(root, text=f"Hire Stray Baker {stray_bakers} - Cost: {upgrade_cost}", font=("Ariel", 12), command=hire_stray)
upgrade_button.pack(pady=10)


def run_autobaker():
    global bread_count, num_baked_stray

    bread_count += stray_bakers * 0.1
    num_baked_stray += stray_bakers * .1

    #counter_label.config(text=f"Bread: {bread_count}")
    root.after(1000, run_autobaker)
    update_ui()

#save_game_state
def save_game_state():
    global bread_count, stray_bakers, upgrade_cost, num_baked_stray, num_baked_gray

    with open("savedata.txt", "w") as f:
        f.write(f"{bread_count}\n{num_baked_gray}\n{stray_bakers}\n{num_baked_stray}\n{upgrade_cost}\n")
    root.after(5000, save_game_state)

    if debug:
        print(f"Game Saved - Bread: {int(bread_count)} Paw-made: {int(num_baked_gray)} Strays: {int(stray_bakers)} Baked by strays: {int(num_baked_stray)} Upgrade Cost: {int(upgrade_cost)} ")

#reset game by changing values to default > overwrite save file > reload game and ui
def reset_game_data():
    global bread_count, stray_bakers, upgrade_cost, num_baked_stray, num_baked_gray

    bread_count = 0
    num_baked_gray = 0
    stray_bakers = 0
    num_baked_stray = 0
    upgrade_cost = 10

    with open("savedata.txt", "w") as f:
        f.write(f"{bread_count}\n{num_baked_gray}\n{stray_bakers}\n{num_baked_stray}\n{upgrade_cost}\n")
    
    load_game_state()
    update_ui()
    print("Game Data Reset")

#reset button
reset_button = tk.Button(root, text="Reset Game", command=reset_game_data)
reset_button.pack(pady=10)

#Update UI buttons - called after run_autobaker(), hire_strays(), and bake_bread()
def update_ui():
    counter_label.config(text=f"Bread: {int(bread_count)}")
    upgrade_button.config(text=f"Hire Stray Baker ({int(stray_bakers)}) - Cost: {int(upgrade_cost)}")

save_game_state()      
run_autobaker()
root.mainloop()