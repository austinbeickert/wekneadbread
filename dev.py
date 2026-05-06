import tkinter as tk
import json
from tkinter import *
from PIL import Image, ImageTk

#Debug switch
debug = 1
debug_click = 1

class Game:
    def __init__(self):
        self.bread_count = 0
        self.stray_baker = 0
        self.upgrade_cost = 10
        self.num_baked_gray = 0
        self.num_baked_stray = 0
        self.lifetime_bread = 0
        self.bps = 0

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
            amount = self.stray_bakers * 0.1
            self.upgrade_cost = int(self.upgrade_cost * 1.15)
            self.bps = amount
    
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
        self.bps = 0

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
gray_baker_click_frame.pack_propagate(False)

def bake_bread_on_click():
    game.bake_bread()
    update_ui()

        #main bake paw button
cat_pil = Image.open("catpaw3.png").convert("RGBA")
cat_image = ImageTk.PhotoImage(cat_pil)
click_paw = tk.Button(gray_baker_click_frame, image=cat_image, command=bake_bread_on_click)
click_paw.image = cat_image
click_paw.pack(pady=(50,0))
        #label "Click for bread"
tk.Label(gray_baker_click_frame, text="Click for bread", bg="gray").pack(padx=10, pady=10)


    #upgrades
gray_baker_upgrade_frame = tk.Frame(gray_baker_frame, width=620, height=620, bg="gray")
gray_baker_upgrade_frame.pack(padx=10, pady=10)
tk.Label(gray_baker_upgrade_frame, text="Upgrades here", bg="gray").pack(padx=10, pady=10)
gray_baker_upgrade_frame.pack_propagate(False)


#right column containers
stray_baker_frame = tk.Frame(main_frame, width=640, bg="DarkOrange1")
stray_baker_frame.pack(side=tk.RIGHT, fill="y", padx=(0,10), pady=10)
stray_baker_frame.pack_propagate(False)

    #title
stray_baker_top_frame = tk.Frame(stray_baker_frame, width=620, height=50, bg="gray")
stray_baker_top_frame.pack(padx=10, pady=5)
tk.Label(stray_baker_top_frame, text="Stray Bakers", bg="gray").pack(padx=10, pady=10)
stray_baker_top_frame.pack_propagate(False)

def hire_stray_on_click():
    game.hire_stray()
    update_ui()

    #image of hire strays
stray_baker_image_frame = tk.Frame(stray_baker_frame, width=620, height=290, bg="gray")
stray_baker_image_frame.pack(padx=10, pady=5)
stray_baker_image_frame.pack_propagate(False)

        #hire stray button
stray_cat_pil = Image.open("bushcat.png").convert("RGBA")
stray_baker_image = ImageTk.PhotoImage(stray_cat_pil)
hire_stray_bakers = tk.Button(stray_baker_image_frame, image=stray_baker_image, command=hire_stray_on_click)
hire_stray_bakers.pack(pady=(20,0))

        #label for stray hire
hire_stray_bakers_label = tk.Label(stray_baker_image_frame, text=f"Hire Stray Baker {game.stray_bakers} - Cost: {game.upgrade_cost}", font=("Ariel", 12), bg="gray")
hire_stray_bakers_label.pack(padx=10,pady=10)

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


#middle column containers
middle_frame = tk.Frame(main_frame, bg="DarkOrange4")
middle_frame.pack(padx=10, pady=10)

#top middle box
bread_count_frame = tk.Frame(middle_frame, width=640, height=400, bg="DarkOrange1")
bread_count_frame.pack(pady=(0,0))
bread_count_frame.pack_propagate(False)

    #bread counter node
counter_label = tk.Label(bread_count_frame, text=f"Bread: {game.bread_count}", bg="DarkOrange1", font=("Ariel", 32))
counter_label.pack(pady=(150,0))

    #bps counter node
per_second_label = tk.Label(bread_count_frame, text=f"per second: {game.bps}", bg="DarkOrange1", font=("Ariel", 16))
per_second_label.pack()

    #reset button
def reset_game_data_on_click():
    game.reset_game_data()
    update_ui()

reset_button = tk.Button(bread_count_frame, text="Reset Game", command=reset_game_data_on_click)
reset_button.pack(pady=10)

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
        #gumbie image
gumbie_image = Image.open("gumbiecat.png").convert("RGBA")
gumbie = ImageTk.PhotoImage(gumbie_image)
gumbie_cat = tk.Button(feed_gumbie_frame, image=gumbie)
gumbie_cat.pack(pady=10)


def save_game_data():
    game.save_game_data()
    root.after(5000, save_game_data)
    if debug:
        print(f"Game Saved - Bread: {int(game.bread_count)}, Paw-made: {int(game.num_baked_gray)}, Strays: {int(game.stray_bakers)}, Baked by strays: {int(game.num_baked_stray)}, Upgrade Cost: {int(game.upgrade_cost)}, BPS: {game.bps:.2f} ")

def run_autobaker_loop():
    game.run_autobaker()
    update_ui()
    root.after(1000, run_autobaker_loop)

def update_ui():
    counter_label.config(text=f"Bread: {game.bread_count:.2f}")
    hire_stray_bakers_label.config(text=f"Hire Stray Baker ({int(game.stray_bakers)}) - Cost: {int(game.upgrade_cost)}")
    per_second_label.config(text=f"per second: {game.bps:.2f}")

update_ui()
save_game_data()
run_autobaker_loop()
root.mainloop()

