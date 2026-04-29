import tkinter as tk
import json
from tkinter import PhotoImage
from PIL import Image, ImageTk

#Debug switch
debug = 1
debug_click = 0

class Game:
    def __init__(self):
        self.bread_count = 0
        self.stray_bakers = 0
        self.upgrade_cost = 10
        self.num_baked_gray = 0
        self.num_baked_stray = 0
        self.lifetime_bread = 0

    def bake_bread(self):
        self.bread_count += 1
        self.num_baked_gray += 1
        self.lifetime_bread += 1
        if debug_click:
            print(f"Bread Baked. Total {self.bread_count}")
    
    def hire_stray(self):
        if self.bread_count >= self.upgrade_cost:
            self.bread_count -= self.upgrade_cost
            self.stray_bakers += 1
            self.upgrade_cost = int(self.upgrade_cost * 1.15)
    
    def run_autobaker(self):
        amount = self.stray_bakers * 0.1
        
        self.bread_count += amount
        self.num_baked_stray += amount
        self.lifetime_bread += amount
    
    def reset_game_data(self):
        self.bread_count = 0
        self.stray_bakers = 0
        self.upgrade_cost = 10
        self.num_baked_gray = 0
        self.num_baked_stray = 0
        self.lifetime_bread = 0

        if debug:
            print("We Knead Bread data RESET")
    
    def save_game_data(self):   
        with open("savedata.txt", "w") as sd:
            json.dump(self.__dict__, sd)
        
        if debug:
            print("We Knead Bread data SAVED")

    def load_game_data(self):      
        try:
            with open("savedata.txt", "r") as sd:
                self.__dict__.update(json.load(sd))
        
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        if debug:
            print("We Knead Bread data LOADED")


game = Game()
game.load_game_data()

#set window, images, and buttons
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
counter_label = tk.Label(root, text=f"Bread: {game.bread_count}", font=("Ariel", 18))
counter_label.pack(pady=20)

def bake_bread_on_click():
    game.bake_bread()
    update_ui()

#main bake paw button
click_paw = tk.Button(root, image=cat_image, command=bake_bread_on_click, borderwidth=0, highlightthickness=0)
click_paw.image = cat_image
click_paw.pack(pady=10)

def hire_stray_on_click():
    game.hire_stray()
    update_ui()

#hire stray button
upgrade_button = tk.Button(root, text=f"Hire Stray Baker {game.stray_bakers} - Cost: {game.upgrade_cost}", font=("Ariel", 12), command=hire_stray_on_click)
upgrade_button.pack(pady=10)

def reset_game_data_on_click():
    game.reset_game_data()
    update_ui()

#reset button
reset_button = tk.Button(root, text="Reset Game", command=reset_game_data_on_click)
reset_button.pack(pady=10)

def update_ui():
    counter_label.config(text=f"Bread: {int(game.bread_count)}")
    upgrade_button.config(text=f"Hire Stray Baker ({int(game.stray_bakers)}) - Cost: {int(game.upgrade_cost)}")

def save_game_data():
    game.save_game_data()
    root.after(5000, save_game_data)
    if debug:
        print(f"Game Saved - Bread: {int(game.bread_count)} Paw-made: {int(game.num_baked_gray)} Strays: {int(game.stray_bakers)} Baked by strays: {int(game.num_baked_stray)} Upgrade Cost: {int(game.upgrade_cost)} ")

def run_autobaker_loop():
    game.run_autobaker()
    update_ui()
    root.after(1000, run_autobaker_loop)

update_ui()
save_game_data()
run_autobaker_loop()
root.mainloop()