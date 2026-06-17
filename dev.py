import tkinter as tk
import json
import random
import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

#Debug switches
debug = 0
debug_click = 0
debug_animate = 1
debug_datetime = 0
debug_daily_stray = 0
debug_overtime = 0
debug_batch_baking = 0
debug_energy = 0
debug_cheats = 1

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
        self.well_rounded_bonus_bake_power_per_level = 0
        self.stray_energy = 0
        self.max_stray_energy = 100.0
        self.energy_regen_rate = 1
        self.energy_regen_interval = 60
        self.last_energy_gain = datetime.datetime.now()
        self.turbo_bake_active = False
        self.turbo_bake_enabled = False
        self.turbo_bake_multiplier = 2
        self.turbo_bake_drain = 1
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
             ),
                'well_rounded': Upgrade (
                    "Well Rounded",
                    100000,
                    well_rounded
                ),
                'turbo_bake': Upgrade (
                    "Turbo Bake",
                    1000,
                    turbo_strays
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
        self.well_rounded_bonus_bake_power_per_level = 0
        self.stray_energy = 0
        self.max_stray_energy = 100.0
        self.energy_regen_rate = 1
        self.energy_regen_interval = 60
        self.last_energy_gain = None
        self.turbo_bake_active = False
        self.turbo_bake_enabled = False
        self.turbo_bake_multiplier = 2
        self.turbo_bake_drain = 1
        

        for up in self.upgrades.values():
            up.cost = up.base_cost
            up.level = 0

        if debug:
            print("We Knead Bread data RESET")

    def bake_bread(self):
        amount, crit = self.calculate_bread_gained_on_click()
        
        self.bread_count += amount
        self.num_baked_gray += amount
        self.lifetime_bread += amount

        self.batch_baking_last_click_time = datetime.datetime.now()

        if debug_animate:
            if crit:
                x = random.randint(25, 100)
                create_floating_text(gray_popup_canvas, f"+{amount:,.1f}", x, 350, "purple")
            else:
                x = random.randint(25, 100)
                create_floating_text(gray_popup_canvas, f"+{amount:,.1f}", x, 350, "white")

        if debug_click:
            print(f"Bread Baked. Total {self.bread_count}, Lifetime Total {self.lifetime_bread}")
            print(f"Kitten Staff bonus: {game.get_kitten_staff_bonus()}")

        if debug_datetime:
            print(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S')}")
            print(self.batch_baking_last_click_time)

        if debug_overtime:
            print(f"Is overtime baking: {self.is_overtime_baking()}")

        # if debug_batch_baking:
        #     print(f"Batch baking last click: {self.batch_baking_last_click_time}")

        return amount
    
    def is_overtime_baking(self):
        current_hour = datetime.datetime.now().hour
        return current_hour >= 17 or current_hour < 9
    
    def calculate_overtime_bonus_ui(self):
        amount = (self.overtime_baking_bonus_multiplier - 1) * 100
        if amount < 50:
            amount = 0
        return amount

    def calculate_well_rounded_bonus(self):
        total_levels = sum(up.level for up in self.upgrades.values())
        bonus = total_levels * self.well_rounded_bonus_bake_power_per_level
        return bonus

    def calculate_bread_gained_on_click(self):
        bread_gained = self.click_power
        crit = False

        #Add well rounded bonus
        if self.upgrades["well_rounded"].level > 0:
            bread_gained += self.calculate_well_rounded_bonus()

        #Get kitten staff bonus
        if self.upgrades["kitten_staff"].level > 0:
            bread_gained += self.get_kitten_staff_bonus()              

        #Purr-fect loaf
        if self.upgrades["purrfect_loaf"].level > 0:
            if self.determine_crit():
                bread_gained *= 2
                crit = True
                print("A PURR-FECT LOAF!")
        
        #Overtime baking
        if self.upgrades["overtime_baking"].level > 0 and self.is_overtime_baking():
            bread_gained *= self.overtime_baking_bonus_multiplier

        #Batch baking
        if self.upgrades["batch_baking"].level > 0 and self.batch_baking_last_click_time is not None:
            time_diff = (datetime.datetime.now() - self.batch_baking_last_click_time).total_seconds()
            if time_diff > 1000: #cap @ +1200%
                time_diff = 1000
            bread_gained *= 1 + (self.batch_baking_multiplier * time_diff)

            if debug_batch_baking:
                print(f"Time since last click: {time_diff} seconds")
                print(f"Batch baking multiplier: {self.batch_baking_multiplier}")
                print(f"Batch baking bonus: {1 + (self.batch_baking_multiplier * time_diff)}")
           
        return bread_gained, crit

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
         amount = (self.stray_baker_count) * self.stray_power
         if self.turbo_bake_active:
             amount *= self.turbo_bake_multiplier
         self.bps = amount

    def run_autobaker(self):
        amount = (self.stray_baker_count) * self.stray_power
        if self.turbo_bake_active:
            amount *= self.turbo_bake_multiplier            
        self.bread_count += amount
        self.num_baked_stray += amount
        self.lifetime_bread += amount
        if debug_batch_baking:
            print(f"Batch baking last click: {self.batch_baking_last_click_time}")

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
    
    def energy_regen(self):
        if self.last_energy_gain is None:
            self.last_energy_gain = datetime.datetime.now()
            return

        if self.stray_energy >= self.max_stray_energy:
            self.stray_energy = self.max_stray_energy
            return
        
        #offline energy regen calculation
        elapsed_time = (datetime.datetime.now() - self.last_energy_gain).total_seconds()
        energy_to_add = elapsed_time // self.energy_regen_interval

        if energy_to_add > 0:
            self.stray_energy += (energy_to_add * self.energy_regen_rate)

            self.stray_energy = min(self.stray_energy, self.max_stray_energy)          
            self.last_energy_gain += datetime.timedelta(seconds=energy_to_add * self.energy_regen_interval)

            if debug_energy:
                print(
                f"Energy regenerated by "
                f"{energy_to_add * self.energy_regen_rate}. "
                f"Current energy: {self.stray_energy}"
            )

    def turbo_bake(self):
        self.turbo_bake_active = not self.turbo_bake_active

        if self.turbo_bake_active:
            print("Turbo Bake ON")
        else:
            print("Turbo Bake OFF")
    
    def update_turbo_bake(self):
        if self.turbo_bake_active == False:
            return
        self.stray_energy -= self.turbo_bake_drain

        if self.stray_energy <= 0:
            self.stray_energy = 0
            self.turbo_bake_active = False

            if debug_energy:
                print("Turbo Bake disabled - no energy")


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
            "batch_baking_last_click_time": self.batch_baking_last_click_time.isoformat() if self.batch_baking_last_click_time else None,
            "well_rounded_bonus_bake_power_per_level": self.well_rounded_bonus_bake_power_per_level,
            "last_energy_gain": self.last_energy_gain.isoformat() if self.last_energy_gain else None,
            "stray_energy": self.stray_energy,
            "max_stray_energy": self.max_stray_energy,
            "energy_regen_rate": self.energy_regen_rate,
            "energy_regen_interval": self.energy_regen_interval,
            "turbo_bake_active": self.turbo_bake_active,
            "turbo_bake_multiplier": self.turbo_bake_multiplier,
            "turbo_bake_drain": self.turbo_bake_drain,
            "turbo_bake_enabled": self.turbo_bake_enabled,
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
            self.well_rounded_bonus_bake_power_per_level = data.get("well_rounded_bonus_bake_power_per_level", 0)
            self.stray_energy = data.get("stray_energy", 0)
            self.max_stray_energy = data.get("max_stray_energy", 100.0)
            self.energy_regen_rate = data.get("energy_regen_rate", 1)
            self.energy_regen_interval = data.get("energy_regen_interval", 60)
            self.turbo_bake_active = data.get("turbo_bake_active", False)
            self.turbo_bake_multiplier = data.get("turbo_bake_multiplier", 2)
            self.turbo_bake_drain = data.get("turbo_bake_drain", 1)
            self.turbo_bake_enabled = data.get('turbo_bake_enabled', False)

            saved_time = data.get("batch_baking_last_click_time")

            if saved_time:
                self.batch_baking_last_click_time = datetime.datetime.fromisoformat(saved_time)
            else:
                self.batch_baking_last_click_time = None

            saved_energy_time = data.get("last_energy_gain")

            if saved_energy_time:
                self.last_energy_gain = datetime.datetime.fromisoformat(saved_energy_time)
            else:
                self.last_energy_gain = datetime.datetime.now()          

            self.energy_regen()


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

def well_rounded(game):
    game.well_rounded_bonus_bake_power_per_level += 1

def turbo_strays(game):
    game.turbo_bake_enabled = True
    game.turbo_bake_multiplier += 1

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

def create_floating_text(canvas,text, x, y, color):
    text_id = canvas.create_text(
        x,
        y,
        text=text,
        fill=color,
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
    update_ui()

def get_lots_of_energy_on_click():
    game.stray_energy = 100
    update_ui()

def update_ui():
    game.calculate_bps()
    counter_label.config(text=f"Bread: {game.bread_count:,.1f}")
    hire_stray_bakers_label.config(text=f"Hire Stray Bakers | Cost: {int(game.stray_baker_upgrade_cost):,.0f}\n You have [{int(game.stray_baker_count)}] stray(s) baking bread each second")
    per_second_label.config(text=f"per second: {game.bps:,.1f}")
    upgrade_button_multi_paw_baking.config(text=f"Multi-Paw Baking | Cost: {game.upgrades['multi_paw_baking'].cost:,.0f} | Level: {game.upgrades['multi_paw_baking'].level}\n Effect: Increase bake power by 1 | (Current: +{game.click_power:,})")
    upgrade_button_purrfect_loaf.config(text=f"Purr-fect Loaf | Cost: {game.upgrades['purrfect_loaf'].cost:,.0f} | Level: {game.upgrades['purrfect_loaf'].level}\n Effect: +1% chance to bake double bread | (Current: {game.crit_chance}%)")
    upgrade_button_kitten_staff.config(text=f"Kitten Staff | Cost: {int(game.upgrades['kitten_staff'].cost):,.0f} | Level: {game.upgrades['kitten_staff'].level}\n Effect: Gain increased bake power per stray baker.\n +5% per level | (Current: +{(game.kitten_staff_multiplier * 100):,.0f}% bonus)")
    upgrade_button_overtime_baking.config(text=f"Overtime Baking | Cost: {game.upgrades['overtime_baking'].cost:,.0f} | Level: {game.upgrades['overtime_baking'].level}\n Effect: Bake 50% more bread after 5pm and before 9am.\n +10% per level | Current: {game.calculate_overtime_bonus_ui():,.0f}% ")
    upgrade_button_batch_baking.config(text=f"Batch Baking | Cost: {game.upgrades['batch_baking'].cost:,.0f} | Level: {game.upgrades['batch_baking'].level}\n Effect: Each second spent not baking increases the next bake by 1%.\n +1% per level | (Current bonus: {game.batch_baking_multiplier * 100:,.0f}%)")
    upgrade_button_well_rounded.config(text=f"Magic Paws | Cost: {game.upgrades['well_rounded'].cost:,.0f} | Level: {game.upgrades['well_rounded'].level}\n Effect: Increase bake power by the cumulative totals of all upgrade levels.\n Additional levels in this upgrade increase the multiplier by 1 per level.\n (Current bonus bake power: +{game.calculate_well_rounded_bonus()})")

    free_stray_upgrade_button.config(text=f"Cat Distribution System | Cost: {game.upgrades['free_stray'].cost:,.0f} | Level: {game.upgrades['free_stray'].level}\n Effect: Gain a number of free stray bakers per day.\n +1 per level | (Found per day: {game.free_stray_amount} | Strays found: {game.free_strays_found}")
    turbo_bake_upgrade_button.config(text=f"Turbo Bakers | Cost: {game.upgrades['turbo_bake'].cost:,.0f} | Level: {game.upgrades['turbo_bake'].level}\n Effect: Unlock the ability to active Turbo Bake mode.\n While active, increase your stray bakers baking power by 2x.\n + 1x per level.")
    # hire_stray_upgrade_button.config(text=f"Hire Stray Bakers | Cost: {int(game.stray_baker_upgrade_cost):,.0f} | Level: {int(game.stray_baker_count)}\n Effect: Hire a stray baker that bakes a bit of bread each second automatically. +1 stray per level\n (Current: {int(game.stray_baker_count)} strays)")
    energy_label.config(text=f"{int(game.stray_energy)} / {game.max_stray_energy} Energy")
    energy_bar['value'] = game.stray_energy

    for key, button in upgrade_buttons.items():
        if game.bread_count >= game.upgrades[key].cost:
            button.config(state="normal")
        else:
            button.config(state="disabled")

    if game.turbo_bake_enabled:
        turbo_bake_button.config(state="normal")
    else:
        turbo_bake_button.config(state="disabled")

    if game.turbo_bake_active:
        turbo_bake_button.config(text="Turbo Bake: ON")
    else:
        turbo_bake_button.config(text="Turbo Bake: OFF")

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
gray_baker_top_frame = tk.Frame(gray_baker_frame, width=620, height=50, bg="DarkOrange1")
gray_baker_top_frame.pack(padx=10, pady=5)
tk.Label(gray_baker_top_frame, text="Head Chef", bg="DarkOrange1").pack(padx=10, pady=10)
gray_baker_top_frame.pack_propagate(False)

    #click button
gray_baker_click_frame = tk.Frame(gray_baker_frame, width=620, height=350, bg="DarkOrange1")
gray_baker_click_frame.pack(padx=10, pady=5)
gray_baker_click_frame.pack_propagate(False)

        #main bake paw button
cat_pil = Image.open("catpaw3.png").convert("RGBA")
cat_image = ImageTk.PhotoImage(cat_pil)
click_paw = tk.Button(gray_baker_click_frame, image=cat_image, command=bake_bread_on_click)
click_paw.image = cat_image
click_paw.pack(pady=(50,0))
        #label "Click for bread"
tk.Label(gray_baker_click_frame, text="Click for bread", bg="DarkOrange1").pack(padx=10, pady=10)

    #upgrades -----------------------------------------------------------------------------------------------------------------
gray_baker_upgrade_frame = tk.Frame(gray_baker_frame, width=620, height=620, bg="DarkOrange1")
gray_baker_upgrade_frame.pack(padx=10, pady=10)
tk.Label(gray_baker_upgrade_frame, text="Upgrades here", bg="DarkOrange1").pack(padx=10, pady=10)

        #multi-paw baking upgrade button
upgrade_button_multi_paw_baking = tk.Button(gray_baker_upgrade_frame,
                                            command=lambda: buy_upgrade(game.upgrades['multi_paw_baking']), bg="DarkOrange1")
upgrade_button_multi_paw_baking.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Purr-fect loaf
upgrade_button_purrfect_loaf = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['purrfect_loaf']), bg="DarkOrange1")
upgrade_button_purrfect_loaf.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Kitten staff
upgrade_button_kitten_staff = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['kitten_staff']), bg="DarkOrange1")
upgrade_button_kitten_staff.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Overtime baking
upgrade_button_overtime_baking = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['overtime_baking']), bg="DarkOrange1")
upgrade_button_overtime_baking.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #Batch baking
upgrade_button_batch_baking = tk.Button(gray_baker_upgrade_frame, 
                                            command=lambda: buy_upgrade(game.upgrades['batch_baking']), bg="DarkOrange1")
upgrade_button_batch_baking.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)

        #new upgrade
upgrade_button_well_rounded = tk.Button(gray_baker_upgrade_frame,
                                        command=lambda: buy_upgrade(game.upgrades['well_rounded']), bg="DarkOrange1")
upgrade_button_well_rounded.pack(padx=10,pady=10)
gray_baker_upgrade_frame.pack_propagate(False)


#right column containers
stray_baker_frame = tk.Frame(main_frame, width=640, bg="DarkOrange1")
stray_baker_frame.pack(side=tk.RIGHT, fill="y", padx=(0,10), pady=10)
stray_baker_frame.pack_propagate(False)

    #title
stray_baker_top_frame = tk.Frame(stray_baker_frame, width=620, height=50, bg="DarkOrange1")
stray_baker_top_frame.pack(padx=10, pady=5)
tk.Label(stray_baker_top_frame, text="Stray Bakers", bg="DarkOrange1").pack(padx=10, pady=10)
stray_baker_top_frame.pack_propagate(False)

    #image of hire strays
stray_baker_image_frame = tk.Frame(stray_baker_frame, width=620, height=290, bg="DarkOrange1")
stray_baker_image_frame.pack(padx=10, pady=5)
stray_baker_image_frame.pack_propagate(False)

        #hire stray button
stray_cat_pil = Image.open("bushcat.png").convert("RGBA")
stray_baker_image = ImageTk.PhotoImage(stray_cat_pil)
hire_stray_bakers = tk.Button(stray_baker_image_frame, image=stray_baker_image, command=hire_stray_on_click)
hire_stray_bakers.pack(pady=(20,0))

        #label for stray hire
hire_stray_bakers_label = tk.Button(stray_baker_image_frame, text=f"Hire Stray Baker {game.stray_baker_count} - Cost: {game.stray_baker_upgrade_cost}", command=hire_stray_on_click, font=("Ariel", 12), bg="DarkOrange1")
hire_stray_bakers_label.pack(padx=10,pady=10)

    #energy
stray_baker_energy_frame = tk.Frame(stray_baker_frame, width=620, height=50, bg="DarkOrange1")
stray_baker_energy_frame.pack(padx=10, pady=5)


energy_bar = ttk.Progressbar(
    stray_baker_energy_frame,
    orient="horizontal",
    length=500,
    mode="determinate",
    maximum=100,
)
energy_bar.pack(pady=5)

energy_label = tk.Label(
    stray_baker_energy_frame,
    text="100 / 100 Energy",
    bg="DarkOrange1"
)
energy_label.pack()

turbo_bake_button = tk.Button(stray_baker_energy_frame, text="Turbo Bake", command=lambda: game.turbo_bake())
turbo_bake_button.pack(pady=5)

    #upgrades -----------------------------------------------------------------------------------------------------------------
stray_baker_upgrade_frame = tk.Frame(stray_baker_frame, width=620, height=620, bg="DarkOrange1")
stray_baker_upgrade_frame.pack(padx=10, pady=10)
tk.Label(stray_baker_upgrade_frame, text="Upgrades here", bg="DarkOrange1").pack(padx=10, pady=10)
stray_baker_upgrade_frame.pack_propagate(False)

    #turbo
turbo_bake_upgrade_button = tk.Button(stray_baker_upgrade_frame, command=lambda: buy_upgrade(game.upgrades['turbo_bake']), bg="DarkOrange1")
turbo_bake_upgrade_button.pack(padx=10, pady=10)

    #cat distribution system
free_stray_upgrade_button = tk.Button(stray_baker_upgrade_frame,
                                        command=lambda: buy_upgrade(game.upgrades['free_stray']), bg="DarkOrange1")
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

if debug_cheats:
    #lots of bread button
    lots_of_bread_button = tk.Button(bread_count_frame, text="Get Lots of Bread", command=get_lots_of_bread_on_click)
    lots_of_bread_button.pack(pady=10)

    lots_of_energy_button = tk.Button(bread_count_frame, text="Get Lots of Energy", command=get_lots_of_energy_on_click)
    lots_of_energy_button.pack(pady=10)

#bottom middle box
gumbie_frame = tk.Frame(middle_frame, width=640, height=660, bg="DarkOrange1")
gumbie_frame.pack(pady=(10,0))

    #gumbie upgrades
gumbie_upgrade_frame = tk.Frame(gumbie_frame, width=620, height=220, bg="DarkOrange1")
gumbie_upgrade_frame.pack(padx=10, pady=(10,0))
tk.Label(gumbie_upgrade_frame, text="Upgrades here", bg="DarkOrange1").pack(padx=10, pady=10)
gumbie_upgrade_frame.pack_propagate(False)

    #feed gumbie button
feed_gumbie_frame = tk.Frame(gumbie_frame, width=620, height=620, bg="DarkOrange1")
feed_gumbie_frame.pack(padx=10, pady=10)
tk.Label(feed_gumbie_frame, text="Feed gumbie", bg="DarkOrange1").pack(padx=10, pady=10)
feed_gumbie_frame.pack_propagate(False)

    #gumbie image
gumbie_image = Image.open("gumbiecat.png").convert("RGBA")
gumbie = ImageTk.PhotoImage(gumbie_image)
gumbie_cat = tk.Button(feed_gumbie_frame, image=gumbie)
gumbie_cat.pack(pady=10)

upgrade_buttons = {
    "multi_paw_baking": upgrade_button_multi_paw_baking,
    "purrfect_loaf": upgrade_button_purrfect_loaf,
    "kitten_staff": upgrade_button_kitten_staff,
    "overtime_baking": upgrade_button_overtime_baking,
    "batch_baking": upgrade_button_batch_baking,
    "well_rounded": upgrade_button_well_rounded,
    "free_stray": free_stray_upgrade_button,
    "turbo_bake": turbo_bake_upgrade_button,
}


def save_game_data():
    game.save_game_data()
    root.after(5000, save_game_data)
    if debug:
        print("------------Game Saved------------")
        for key, value in game.get_save_data().items():
            print(f"{key}: {value}")

def run_autobaker_loop():
    game.run_autobaker()
    game.update_turbo_bake()
    game.check_daily_stray()
    game.energy_regen()
    update_ui()
    root.after(1000, run_autobaker_loop)

update_ui()
save_game_data()
run_autobaker_loop()
root.mainloop()

