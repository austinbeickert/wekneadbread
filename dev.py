import tkinter as tk
import json
import random
from tkinter import *
from PIL import Image, ImageTk

#Debug switches
debug = 0
debug_click = 0
debug_animate = 1

class Upgrade: 
    def __init__(self, name, base_cost, effect):
        self.name = name
        self.base_cost = base_cost
        self.cost = base_cost
        self.effect = effect
        self.level = 0      


    def buy(self, game):
        if debug:
            print("Trying to buy upgrade...")
        if game.bread_count >= self.cost:
            game.bread_count -= self.cost 

            self.effect(game)

            self.level += 1

            self.cost = round(self.cost * 1.5)

            if debug:
                print(f"{self.name} bought")
                print(f"Level: {self.level}")
                print(f"New cost: {self.cost}")
                print(f"Click power: {game.click_power}")

class Game:
    def __init__(self):
        self.bread_count = 0
        self.stray_baker_count = 0
        self.stray_baker_upgrade_cost = 10
        self.num_baked_gray = 0
        self.num_baked_stray = 0
        self.lifetime_bread = 0
        self.bps = 0
        self.click_power = 1
        self.stray_power = 0.1
        self.crit_chance = 0
        self.kitten_staff_multiplier = 0.05
        self.upgrades = {
            "multi_paw_baking": Upgrade (
                "Multi-Paw Baking",
                500,
                multi_paw_baking
             ),
             "purrfect_loaf": Upgrade (
                 "Purr-fect Loaf",
                 1000,
                 purrfect_loaf
             ),
             "kitten_staff": Upgrade (
                 "Kitten Staff",
                 1500,
                 kitten_staff
             ),
        }

    def reset_game_data(self):
        self.bread_count = 0
        self.stray_baker_count = 0
        self.stray_baker_upgrade_cost = 10
        self.num_baked_gray = 0
        self.num_baked_stray = 0
        self.lifetime_bread = 0
        self.bps = 0
        self.click_power = 1
        self.stray_power = 0.1
        self.crit_chance = 0
        self.kitten_staff_multiplier = 0.05

        for up in self.upgrades.values():
            up.cost = up.base_cost
            up.level = 0

        if debug:
            print("We Knead Bread data RESET")

    def bake_bread(self):
        amount = self.calculate_bread_gained_on_click()

        self.bread_count += amount
        self.num_baked_gray += amount
        self.lifetime_bread += amount

        if debug_animate:
            x = random.randint(25, 100)
            create_floating_text(gray_popup_canvas, f"+{amount:,.1f}", x, 350)

        if debug_click:
            print(f"Bread Baked. Total {self.bread_count}, Lifetime Total {self.lifetime_bread}")
            print(f"Kitten Staff bonus: {game.get_kitten_staff_bonus()}")

        return amount
    
    def calculate_bread_gained_on_click(self):
        bread_gained = self.click_power
        #Get kitten staff bonus
        if self.upgrades["kitten_staff"].level > 0:
            bread_gained += self.get_kitten_staff_bonus()     
            

        #Purr-fect loaf
        if self.upgrades["purrfect_loaf"].level > 0:
            if self.determine_crit():
                bread_gained *= 2
                print("A PURR-FECT LOAF!")
        
        return bread_gained
 
    
    def get_kitten_staff_bonus(self):
        return self.stray_baker_count * self.kitten_staff_multiplier
    
    def determine_crit(self):
        return random.randint(1,100) <= self.crit_chance


    def hire_stray(self):
        if self.bread_count >= self.stray_baker_upgrade_cost:
            self.bread_count -= self.stray_baker_upgrade_cost
            self.stray_baker_count += 1
            amount = self.stray_baker_count * self.stray_power
            self.stray_baker_upgrade_cost = int(self.stray_baker_upgrade_cost * 1.15)
            self.bps = amount
    
    def run_autobaker(self):
        amount = self.stray_baker_count * self.stray_power      
        self.bread_count += amount
        self.num_baked_stray += amount
        self.lifetime_bread += amount          
    
    def get_save_data(self):
        return {
            "bread_count": self.bread_count,
            "stray_baker_count": self.stray_baker_count,
            "stray_baker_upgrade_cost": self.stray_baker_upgrade_cost,
            "num_baked_gray": self.num_baked_gray,
            "num_baked_stray": self.num_baked_stray,
            "lifetime_bread": self.lifetime_bread,
            "bps": self.bps,
            "click_power": self.click_power,
            "stray_power": self.stray_power,

            "upgrades":{
                key: {
                    "level": up.level,
                    "cost": up.cost
                }
                for key, up in self.upgrades.items()
            }
        }

    def save_game_data(self):
        with open("savedata.txt", "w") as sd:
            json.dump(self.get_save_data(), sd)
        
        if debug:
            print("We Knead Bread data SAVED")

          
    def load_game_data(self):
        try:
            with open("savedata.txt", "r") as sd:
                data = json.load(sd)

            # game values
            self.bread_count = data.get("bread_count", 0)
            self.stray_baker_count = data.get("stray_baker_count", 0)
            self.stray_baker_upgrade_cost = data.get("stray_baker_upgrade_cost", 10)
            self.num_baked_gray = data.get("num_baked_gray", 0)
            self.num_baked_stray = data.get("num_baked_stray", 0)
            self.lifetime_bread = data.get("lifetime_bread", 0)
            self.bps = data.get("bps", 0)
            self.click_power = data.get("click_power", 1)
            self.stray_power = data.get("stray_power", 0.1)

            # upgrades
            upgrade_data = data.get("upgrades", {})
            for key, up in self.upgrades.items():
                if key in upgrade_data:
                    up.level = upgrade_data[key].get("level", 0)
                    up.cost = upgrade_data[key].get("cost", up.base_cost)

        except (FileNotFoundError, json.JSONDecodeError):
            pass
        if debug:
            print("We Knead Bread data LOADED")

def multi_paw_baking(game):
    game.click_power += 1

def purrfect_loaf(game):
    game.crit_chance += 1

def kitten_staff(game):
    game.kitten_staff_multiplier += 0.05

game = Game()
game.load_game_data()

def buy_upgrade(upgrade):
    upgrade.buy(game)
    update_ui()

def bake_bread_on_click():
    game.bake_bread()
    update_ui()

def hire_stray_on_click():
    game.hire_stray()
    update_ui()

def reset_game_data_on_click():
    game.reset_game_data()
    update_ui()

def create_floating_text(canvas,text, x, y):
    text_id = canvas.create_text(
        x,
        y,
        text=text,
        fill="white",
        font=("Arial", 16, "bold")
    )
    animate_floating_text(canvas, text_id)

def animate_floating_text(canvas, text_id):
    canvas.move(text_id, 0, -2)

    y = canvas.coords(text_id)[1]

    if y > 10:
        canvas.after(10, lambda: animate_floating_text(canvas, text_id))
    else:
        canvas.delete(text_id)


def update_ui():
    counter_label.config(text=f"Bread: {game.bread_count:,.1f}")
    hire_stray_bakers_label.config(text=f"You have {int(game.stray_baker_count)} strays baking bread\n Cost: {int(game.stray_baker_upgrade_cost):,.2f}")
    per_second_label.config(text=f"per second: {game.bps:,.1f}")
    upgrade_button_multi_paw_baking.config(text=f"Multi-Paw Baking | Cost: {game.upgrades['multi_paw_baking'].cost:,.0f}\n Increase click power by [+{game.click_power:,}]")
    upgrade_button_purrfect_loaf.config(text=f"Purr-fect Loaf | Cost: {game.upgrades['purrfect_loaf'].cost:,.0f}\n [{game.crit_chance}%] chance to bake double bread")
    upgrade_button_kitten_staff.config(text=f"Kitten Staff | Cost: {int(game.upgrades['kitten_staff'].cost):,.0f}\n Click power increased by [{game.kitten_staff_multiplier * 100:,.0f}%] of your stray bakers.")


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

        #multi-paw baking upgrade button
upgrade_button_multi_paw_baking = tk.Button(gray_baker_upgrade_frame,
                                            command=lambda: buy_upgrade(game.upgrades['multi_paw_baking']))
upgrade_button_multi_paw_baking.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Purr-fect loaf
upgrade_button_purrfect_loaf = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['purrfect_loaf']))
upgrade_button_purrfect_loaf.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Kitten staff
upgrade_button_kitten_staff = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['kitten_staff']))
upgrade_button_kitten_staff.pack(padx=10,pady=10)
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
hire_stray_bakers_label = tk.Label(stray_baker_image_frame, text=f"Hire Stray Baker {game.stray_baker_count} - Cost: {game.stray_baker_upgrade_cost}", font=("Ariel", 12), bg="gray")
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

#gray popup canvas
gray_popup_canvas = tk.Canvas(
    middle_frame,
    width=120,
    height=400,
    bg="DarkOrange1",
    highlightthickness=0
)

gray_popup_canvas.place(relx=0.0)

    #bread counter node
counter_label = tk.Label(bread_count_frame, text=f"Bread: {game.bread_count}", bg="DarkOrange1", font=("Ariel", 32))
counter_label.pack(pady=(150,0))

    #bps counter node
per_second_label = tk.Label(bread_count_frame, text=f"per second: {game.bps}", bg="DarkOrange1", font=("Ariel", 16))
per_second_label.pack()

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
        print("------------Game Saved------------")
        for key, value in game.get_save_data().items():
            print(f"{key}: {value}")

def run_autobaker_loop():
    game.run_autobaker()
    update_ui()
    root.after(1000, run_autobaker_loop)


update_ui()
save_game_data()
run_autobaker_loop()
root.mainloop()

