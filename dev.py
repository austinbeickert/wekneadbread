import tkinter as tk
import json
import random
import datetime
from tkinter import *
from PIL import Image, ImageTk

#Debug switches
debug = 0
debug_click = 0
debug_animate = 1
debug_datetime = 0
debug_daily_stray = 0
debug_overtime = 0
debug_batch_baking = 1

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
        self.kitten_staff_multiplier = 0.00
        self.last_free_stray_date = None
        self.free_strays_found = 0
        self.free_stray_amount = 0
        self.overtime_baking_bonus_multiplier = 1.4
        self.batch_baking_multiplier = 0
        self.batch_baking_last_click_time = datetime.datetime.now()

        self.upgrades = {
            "multi_paw_baking": Upgrade (
                "Multi-Paw Baking",
                100,
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
             "free_stray": Upgrade (
                 "Cat Distribution System",
                 2000,
                 free_stray
             ),
             "overtime_baking": Upgrade (
                 "Overtime Baking",
                 5000,
                 overtime_baking
             ),
             'batch_baking': Upgrade (
                 "Batch Baking",
                 10000,
                 batch_baking
             )
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
        self.kitten_staff_multiplier = 0.00
        self.free_strays_found = 0
        self.free_stray_amount = 0
        self.last_free_stray_date = None
        self.overtime_baking_bonus_multiplier = 1.4
        self.batch_baking_multiplier = 0
        self.batch_baking_last_click_time = None

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

        self.batch_baking_last_click_time = datetime.datetime.now()

        if debug_animate:
            x = random.randint(25, 100)
            create_floating_text(gray_popup_canvas, f"+{amount:,.1f}", x, 350)

        if debug_click:
            print(f"Bread Baked. Total {self.bread_count}, Lifetime Total {self.lifetime_bread}")
            print(f"Kitten Staff bonus: {game.get_kitten_staff_bonus()}")

        if debug_datetime:
            print(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}")
            print(self.batch_baking_last_click_time)

        if debug_overtime:
            print(f"Is overtime baking: {self.is_overtime_baking()}")

        if debug_batch_baking:
            print(f"Batch baking last click: {self.batch_baking_last_click_time}")

        return amount
    
    def is_overtime_baking(self):
        current_hour = datetime.datetime.now().hour
        return current_hour >= 17 or current_hour < 9
    
    def calculate_overtime_bonus_ui(self):
        amount = (self.overtime_baking_bonus_multiplier - 1) * 100
        if amount < 50:
            amount = 0
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
        
        #Overtime baking
        if self.upgrades["overtime_baking"].level > 0 and self.is_overtime_baking():
            bread_gained *= self.overtime_baking_bonus_multiplier

        #Batch baking
        if self.upgrades["batch_baking"].level > 0 and self.batch_baking_last_click_time is not None:
            time_diff = (datetime.datetime.now() - self.batch_baking_last_click_time).total_seconds()
            if time_diff > 1200: #cap the batch baking bonus at 1200 seconds (20 minutes / +1200%)
                time_diff = 1200
            bread_gained *= 1 + (self.batch_baking_multiplier * time_diff)

            if debug_batch_baking:
                print(f"Time since last click: {time_diff} seconds")
                print(f"Batch baking multiplier: {self.batch_baking_multiplier}")
                print(f"Batch baking bonus: {1 + (self.batch_baking_multiplier * time_diff)}")

            
        return bread_gained

    def get_kitten_staff_bonus(self):
        return self.stray_baker_count * self.kitten_staff_multiplier
    
    def determine_crit(self):
        return random.randint(1,100) <= self.crit_chance

    def hire_stray(self):
        if self.bread_count >= self.stray_baker_upgrade_cost:
            self.bread_count -= self.stray_baker_upgrade_cost
            self.stray_baker_count += 1
            self.stray_baker_upgrade_cost = int(self.stray_baker_upgrade_cost * 1.15)
    
    def calculate_bps(self):
        self.bps = (self.stray_baker_count) * self.stray_power

    def run_autobaker(self):
        amount = (self.stray_baker_count) * self.stray_power
        self.bread_count += amount
        self.num_baked_stray += amount
        self.lifetime_bread += amount

    def check_daily_stray(self):
        if debug_daily_stray:
            print("Checking for daily stray...")
        if self.upgrades["free_stray"].level == 0:
            return

        today = str(datetime.date.today())

        if debug_daily_stray:
            print(f"Last free stray date: {self.last_free_stray_date}, Today: {today}")

        if self.last_free_stray_date != today:
            self.free_strays_found += self.free_stray_amount
            self.stray_baker_count += self.free_stray_amount
            self.last_free_stray_date = today
            self.save_game_data()
            if debug_daily_stray:
                print(
                    f"Cat Distribution System has been activated!"
                    f"+{self.free_stray_amount} stray(s)!"
                )   
    
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
            "crit_chance": self.crit_chance,
            "kitten_staff_multiplier": self.kitten_staff_multiplier,
            "free_strays_found": self.free_strays_found,
            "free_stray_amount": self.free_stray_amount,
            "last_free_stray_date": self.last_free_stray_date,
            "overtime_baking_bonus_multiplier": self.overtime_baking_bonus_multiplier,
            "batch_baking_multiplier": self.batch_baking_multiplier,
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
            self.crit_chance = data.get("crit_chance", 0)
            self.kitten_staff_multiplier = data.get("kitten_staff_multiplier", 0.0)
            self.free_strays_found = data.get("free_strays_found", 0)
            self.free_stray_amount = data.get("free_stray_amount", 0)
            self.last_free_stray_date = data.get("last_free_stray_date", None)
            self.overtime_baking_bonus_multiplier = data.get("overtime_baking_bonus_multiplier", 1.4)
            self.batch_baking_multiplier = data.get("batch_baking_multiplier", 0.0)

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

#upgrade stat changes
def multi_paw_baking(game):
    game.click_power += 1

def purrfect_loaf(game):
    game.crit_chance += 1

def kitten_staff(game):
    game.kitten_staff_multiplier += 0.05

def free_stray(game):
    game.free_stray_amount += 1
    
def overtime_baking(game):
    game.overtime_baking_bonus_multiplier += 0.1

def batch_baking(game):
    game.batch_baking_multiplier += 0.01

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

def get_lots_of_bread_on_click():
    game.bread_count += 1000000

def update_ui():
    game.calculate_bps()
    counter_label.config(text=f"Bread: {game.bread_count:,.1f}")
    hire_stray_bakers_label.config(text=f"You have {int(game.stray_baker_count)} strays baking bread\n Cost: {int(game.stray_baker_upgrade_cost):,.2f}")
    per_second_label.config(text=f"per second: {game.bps:,.1f}")
    upgrade_button_multi_paw_baking.config(text=f"Multi-Paw Baking | Cost: {game.upgrades['multi_paw_baking'].cost:,.0f} | Level: {game.upgrades['multi_paw_baking'].level}\n Effect: Increase bake power by 1 | (Current: +{game.click_power:,})")
    upgrade_button_purrfect_loaf.config(text=f"Purr-fect Loaf | Cost: {game.upgrades['purrfect_loaf'].cost:,.0f} | Level: {game.upgrades['purrfect_loaf'].level}\n Effect: +1% chance to bake double bread | (Current: {game.crit_chance}%)")
    upgrade_button_kitten_staff.config(text=f"Kitten Staff | Cost: {int(game.upgrades['kitten_staff'].cost):,.0f} | Level: {game.upgrades['kitten_staff'].level}\n Effect: Gain increased bake power per stray baker. +5% per level | (Current: +{(game.kitten_staff_multiplier * 100):,.0f}% bonus)")
    upgrade_button_overtime_baking.config(text=f"Overtime Baking | Cost: {game.upgrades['overtime_baking'].cost:,.0f} | Level: {game.upgrades['overtime_baking'].level}\n Effect: Bake 50% more bread after 5pm and before 9am. +10% per level\n Current: {game.calculate_overtime_bonus_ui():,.0f}% | Overtime hours active?: {game.is_overtime_baking()}")
    upgrade_button_batch_baking.config(text=f"Batch Baking | Cost: {game.upgrades['batch_baking'].cost:,.0f} | Level: {game.upgrades['batch_baking'].level}\n Effect: Each second spent not baking increases the next bake by 1%. +1% per level | (Current bonus: {game.batch_baking_multiplier * 100:,.0f}%)")

    free_stray_upgrade_button.config(text=f"Cat Distribution System | Cost: {game.upgrades['free_stray'].cost:,.0f} | Level: {game.upgrades['free_stray'].level}\n Effect: Gain a number of free stray bakers per day. +1 per level\n (Found per day: {game.free_stray_amount} | Strays found: {game.free_strays_found}")
    hire_stray_upgrade_button.config(text=f"Hire Stray Bakers | Cost: {int(game.stray_baker_upgrade_cost):,.0f} | Level: {int(game.stray_baker_count)}\n Effect: Hire a stray baker that bakes a bit of bread each second automatically. +1 stray per level\n (Current: {int(game.stray_baker_count)} strays)")

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

    #upgrades -----------------------------------------------------------------------------------------------------------------
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

        #Overtime baking
upgrade_button_overtime_baking = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['overtime_baking']))
upgrade_button_overtime_baking.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Batch baking
upgrade_button_batch_baking = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['batch_baking']))
upgrade_button_batch_baking.pack(padx=10,pady=10)
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

    #upgrades -----------------------------------------------------------------------------------------------------------------
stray_baker_upgrade_frame = tk.Frame(stray_baker_frame, width=620, height=620, bg="gray")
stray_baker_upgrade_frame.pack(padx=10, pady=10)
tk.Label(stray_baker_upgrade_frame, text="Upgrades here", bg="gray").pack(padx=10, pady=10)
stray_baker_upgrade_frame.pack_propagate(False)

    #hire_stray_duplicate button
hire_stray_upgrade_button = tk.Button(stray_baker_upgrade_frame,command=lambda: hire_stray_on_click())
hire_stray_upgrade_button.pack(padx=10, pady=10)

    #cat distribution system
free_stray_upgrade_button = tk.Button(stray_baker_upgrade_frame,
                                        command=lambda: buy_upgrade(game.upgrades['free_stray']))
free_stray_upgrade_button.pack(padx=10, pady=10)

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

    #reset button
reset_button = tk.Button(bread_count_frame, text="Reset Game", command=reset_game_data_on_click)
reset_button.pack(pady=10)

    #lots of bread button
lots_of_bread_button = tk.Button(bread_count_frame, text="Get Lots of Bread", command=get_lots_of_bread_on_click)
lots_of_bread_button.pack(pady=10)

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
    game.check_daily_stray()
    update_ui()
    root.after(1000, run_autobaker_loop)

update_ui()
save_game_data()
run_autobaker_loop()
root.mainloop()

