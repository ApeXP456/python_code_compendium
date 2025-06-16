# Written by Jarod L. Cunningham
# NeverDie RPG with GUI using Tkinter (Battle Options: Attack, Run, Use Potion)

import json
import random
import tkinter as tk
from tkinter import messagebox

# ------------------- Character Class -------------------
class Character:
    def __init__(self, name=None, char_class=None, strength=0, intelligence=0, agility=0,
                 max_health=100, current_health=100, inventory=None, gold=0, xp=0, level=1):
        self.name = name or "Unknown"
        self.char_class = char_class or "None"
        self.strength = strength
        self.intelligence = intelligence
        self.agility = agility
        self.max_health = max_health
        self.current_health = current_health if current_health else max_health
        self.inventory = inventory if inventory else ["health potion", "health potion", "sword", "map"]
        self.gold = gold
        self.xp = xp
        self.level = level

    def gain_xp(self, amount):
        self.xp += amount
        level_threshold = 100 * self.level
        if self.xp >= level_threshold:
            self.level += 1
            self.max_health += 10
            self.current_health = self.max_health
            return True
        return False

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def use_potion(self):
        if "health potion" in self.inventory:
            self.heal(30)
            self.inventory.remove("health potion")
            return True
        return False

# ------------------- World Map -------------------
WORLD_MAP = {
    "Cave Entrance": {
        "description": "A dark and mossy cave mouth.",
        "visited": False,
        "boss_defeated": False,
        "boss": {
            "name": "Stonefang the Earthbound",
            "description": "A hulking troll with stone-like skin.",
            "reward": {"gold": 300, "item": "Trollhide Armor"}
        }
    },
    "Crystal Lake": {
        "description": "A shimmering lake filled with glowing water.",
        "visited": False,
        "boss_defeated": False,
        "boss": {
            "name": "Naiadra the Drowned",
            "description": "A ghostly spirit who haunts the lake’s surface.",
            "reward": {"gold": 500, "item": "Water Crystal"}
        }
    },
    "Forgotten Shrine": {
        "description": "Ruins of an ancient shrine to a lost god.",
        "visited": False,
        "boss_defeated": False,
        "boss": {
            "name": "Ashar the Blinded Prophet",
            "description": "A mad oracle who whispers forbidden truths.",
            "reward": {"gold": 600, "item": "Oracle's Eye"}
        }
    },
    "Goblin Camp": {
        "description": "Tents and bonfires of restless goblins.",
        "visited": False,
        "boss_defeated": False,
        "boss": {
            "name": "Grizzle the War Chief",
            "description": "A massive goblin wearing makeshift armor.",
            "reward": {"gold": 400, "item": "War Chief's Blade"}
        }
    },
    "Dragon's Lair": {
        "description": "You can feel the heat. A dragon lives here.",
        "visited": False,
        "boss_defeated": False,
        "boss": {
            "name": "Vulkrath the Flame Wyrm",
            "description": "An ancient dragon wreathed in fire.",
            "reward": {"gold": 1000, "item": "Heart of Flame"}
        }
    }
}

# ------------------- GUI Game Class -------------------
class NeverDieGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeverDie RPG")

        self.main_frame = tk.Frame(root, padx=20, pady=20, bg="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True)

        self.output_text = tk.Text(self.main_frame, height=15, bg="#121212", fg="white")
        self.output_text.pack(fill="both")

        self.choice_frame = tk.Frame(self.main_frame, pady=10)
        self.choice_frame.pack()

        self.character = None
        self.init_game()

    def write(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def clear_choices(self):
        for widget in self.choice_frame.winfo_children():
            widget.destroy()

    def init_game(self):
        self.write("Welcome to NeverDie!")
        self.clear_choices()
        tk.Button(self.choice_frame, text="New Game", command=self.new_game).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Load Game", command=self.load_game).pack(side="left", padx=5)

    def new_game(self):
        self.clear_choices()
        self.write("Enter your character name:")
        self.name_entry = tk.Entry(self.choice_frame)
        self.name_entry.pack(side="left")
        tk.Button(self.choice_frame, text="Next", command=self.choose_class).pack(side="left")

    def choose_class(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required.")
            return
        self.character_name = name
        self.clear_choices()
        self.write("Choose your class:")
        for cls in ["Warrior", "Mage", "Rogue"]:
            tk.Button(self.choice_frame, text=cls, command=lambda c=cls: self.assign_attributes(c)).pack(side="left", padx=5)

    def assign_attributes(self, char_class):
        self.char_class = char_class
        self.clear_choices()
        self.write("Distribute 15 points between Strength, Intelligence, and Agility.")

        self.remaining_points = 15
        self.attr_vars = {attr: tk.IntVar(value=0) for attr in ["Strength", "Intelligence", "Agility"]}

        for attr in self.attr_vars:
            row = tk.Frame(self.choice_frame)
            row.pack()
            tk.Label(row, text=attr).pack(side="left")
            tk.Spinbox(row, from_=0, to=15, textvariable=self.attr_vars[attr], width=5, command=self.update_points).pack(side="left")

        self.points_label = tk.Label(self.choice_frame, text="Points remaining: 15")
        self.points_label.pack()
        tk.Button(self.choice_frame, text="Create Character", command=self.create_character).pack()

    def update_points(self):
        used = sum(var.get() for var in self.attr_vars.values())
        self.remaining_points = 15 - used
        self.points_label.config(text=f"Points remaining: {self.remaining_points}")

    def create_character(self):
        self.update_points()
        if self.remaining_points < 0:
            messagebox.showerror("Error", "You allocated too many points.")
            return

        self.character = Character(
            name=self.character_name,
            char_class=self.char_class,
            strength=self.attr_vars["Strength"].get(),
            intelligence=self.attr_vars["Intelligence"].get(),
            agility=self.attr_vars["Agility"].get()
        )
        self.clear_choices()
        self.write(f"Character created: {self.character.name}, the {self.character.char_class}")
        self.write(f"STR: {self.character.strength}, INT: {self.character.intelligence}, AGI: {self.character.agility}")
        self.show_main_menu()  # shown only if boss already defeated

    def show_main_menu(self):
        self.clear_choices()
        self.write("\nMain Menu")
        tk.Button(self.choice_frame, text="Inventory", command=self.show_inventory).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Use Potion", command=self.use_potion).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Explore Map", command=self.explore_map).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Save Game", command=self.save_game).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Exit", command=self.root.quit).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Visit Merchant", command=self.visit_merchant).pack(side="left", padx=5)

    def show_inventory(self):
        self.write("\nInventory:")
        for item in self.character.inventory:
            self.write(f"- {item}")
        self.write(f"Level: {self.character.level}  |  XP: {self.character.xp}")
        self.show_xp_bar()
        self.write(f"Gold: {self.character.gold}")
        self.write(f"Health: {self.character.current_health}/{self.character.max_health}")

    def use_potion(self):
        if self.character.use_potion():
            self.write("You used a health potion and restored 30 HP.")
        else:
            self.write("No potions available.")

    def explore_map(self):
        self.clear_choices()
        self.write("--- World Map ---")
        tk.Button(self.choice_frame, text="Visit Merchant", command=self.visit_merchant).pack(fill="x", pady=2)
        self.clear_choices()
        self.write("\n--- World Map ---")
        for i, (loc, data) in enumerate(WORLD_MAP.items(), 1):
            status = " (visited)" if data["visited"] else ""
            btn = tk.Button(self.choice_frame, text=f"{i}. {loc}{status}", command=lambda l=loc: self.visit_location(l))
            btn.pack(fill="x", pady=2)

    def visit_location(self, location):
        data = WORLD_MAP[location]
        if not data["visited"]:
            self.write(f"\nYou arrive at {location}. {data['description']}")
            data["visited"] = True
        if not data["boss_defeated"]:
            if "boss_hp" not in data:
                data["boss_hp"] = 120
            self.start_boss_fight(data)
            return
        else:
            self.write(f"You have already defeated the boss of {location}.")
        self.show_main_menu()

    def start_boss_fight(self, location_data):
        boss = location_data["boss"]
        self.write(f"\nA boss appears: {boss['name']} — {boss['description']}")

        def fight_turn():
            self.clear_choices()
            self.write(f"\nYour HP: {self.character.current_health}/{self.character.max_health} | Boss HP: {location_data['boss_hp']}")
            tk.Button(self.choice_frame, text="Attack", command=lambda: self.attack_boss(boss, location_data, fight_turn)).pack(side="left", padx=5)
            tk.Button(self.choice_frame, text="Use Potion", command=lambda: self.use_potion_and_continue(fight_turn)).pack(side="left", padx=5)
            tk.Button(self.choice_frame, text="Run", command=lambda: self.run_from_battle(location_data)).pack(side="left", padx=5)

        fight_turn()

    def attack_boss(self, boss, location_data, callback):
        hit_roll = random.randint(1, 20) + self.character.strength
        if hit_roll >= 17:
            damage = 25
            location_data["boss_hp"] -= damage
            self.write(f"You hit {boss['name']} for {damage} damage!")
        else:
            self.write(f"You missed {boss['name']}.")

        if location_data["boss_hp"] <= 0:
            self.win_boss_fight(location_data)
            return

        enemy_roll = random.randint(1, 20) + 6
        if enemy_roll >= 15:
            self.character.take_damage(18)
            self.write(f"{boss['name']} hits you for 18 damage!")
        else:
            self.write(f"{boss['name']} missed!")

        if self.character.current_health <= 0:
            self.write("You have been defeated. Game Over.")
            self.clear_choices()
            tk.Button(self.choice_frame, text="Start New Game", command=self.new_game).pack(side="left", padx=5)
            tk.Button(self.choice_frame, text="Load Save", command=self.load_game).pack(side="left", padx=5)
        else:
            callback()

    def use_potion_and_continue(self, callback):
        self.use_potion()
        callback()

    def win_boss_fight(self, location_data):
        boss = location_data["boss"]
        reward = boss["reward"]
        self.character.gold += reward["gold"]
        self.character.inventory.append(reward["item"])
        self.write(f"You defeated {boss['name']} and received {reward['gold']} gold and {reward['item']}!")
        location_data["boss_defeated"] = True
        leveled_up = self.character.gain_xp(100)
        self.write("You gained 100 XP!")
        if leveled_up:
            self.write(f"You leveled up to Level {self.character.level}! Max HP increased.")
        self.show_main_menu()

    def save_game(self):
        with open('game_save.json', 'w') as file:
            json.dump(self.character.__dict__, file)
        self.write("Game saved successfully.")

    def load_game(self):
        try:
            with open('game_save.json', 'r') as file:
                data = json.load(file)
                self.character = Character(**data)
                self.write(f"Game loaded. Welcome back, {self.character.name}!")
                self.show_main_menu()
        except FileNotFoundError:
            self.write("No save file found.")

    def visit_merchant(self):
        self.clear_choices()
        self.write(f"Welcome to the Merchant!\nLevel: {self.character.level}  |  Gold: {self.character.gold}")
        self.write("Each health potion costs 100 gold.")
        self.show_xp_bar()
        tk.Button(self.choice_frame, text="Buy Potion (100g)", command=self.buy_potion).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Sell Items", command=self.sell_items).pack(side="left", padx=5)
        tk.Button(self.choice_frame, text="Back to Menu", command=self.show_main_menu).pack(side="left", padx=5)

    def buy_potion(self):
        if self.character.gold >= 100:
            self.character.gold -= 100
            self.character.inventory.append("health potion")
            self.write("You bought a health potion!")
        else:
            self.write("Not enough gold.")

    def show_xp_bar(self):
        bar_length = 20
        xp = self.character.xp
        level = self.character.level
        threshold = 100 * level
        filled = int((xp / threshold) * bar_length)
        bar = '[' + '=' * filled + ' ' * (bar_length - filled) + f'] {xp}/{threshold} XP'
        self.write(bar)

    def sell_items(self):
        self.clear_choices()
        self.write("Sellable Items:")
        sellable_items = [item for item in self.character.inventory if item not in ["health potion", "sword", "map"]]
        if not sellable_items:
            self.write("You have no items to sell.")
            tk.Button(self.choice_frame, text="Back", command=self.visit_merchant).pack()
            return
        for item in sellable_items:
            tk.Button(self.choice_frame, text=f"Sell {item} (+100g)", command=lambda i=item: self.sell_item(i)).pack(fill="x", padx=5, pady=2)
        tk.Button(self.choice_frame, text="Back", command=self.visit_merchant).pack(pady=5)

    def sell_item(self, item):
        self.character.inventory.remove(item)
        self.character.gold += 100
        self.write(f"You sold {item} for 100 gold.")
        self.sell_items()

    def run_from_battle(self, location_data):
        self.write("You ran away from battle!")
        location_data.pop("boss_hp", None)
        self.show_main_menu()

# ------------------- Start GUI Game -------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = NeverDieGUI(root)
    root.mainloop()
