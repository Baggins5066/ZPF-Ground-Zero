import random
import time

# Prints text slowly, character by character, for dramatic effect
def slow_print(text, delay=0.02):
    for c in text:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()

# Prompts the user to choose from a set of options, returns the selected key
def choose(prompt, options):
    while True:
        slow_print(prompt)
        for key, desc in options.items():
            slow_print(f"{key}) {desc}")
        choice = input("> ").strip()
        if choice in options:
            return choice
        slow_print("Invalid entry.")

# Player class holds all player stats and inventory
class Player:
    def __init__(self):
        self.health = 8
        self.max_health = 8
        self.hunger = 10
        self.luck = 0
        self.damage = 1
        self.money = 10
        self.wood = 0
        self.stone = 0
        self.machineparts = 0
        self.fishingrod = "Stick And String"
        self.weapon = "Fists"
        self.armor = []
        self.fish = []
        self.cookbook = False
        self.name = ""
        self.location = "Forest"
        self.turns = 0

    # Prints current player stats
    def stats(self):
        print(f"\nNAME: {self.name}")
        print(f"HEALTH: {self.health}/{self.max_health}")
        print(f"DAMAGE: {self.damage}")
        print(f"LUCK: {self.luck}")
        print(f"HUNGER: {self.hunger}")
        print(f"MONEY: {self.money}")
        print(f"WOOD: {self.wood}")
        print(f"STONE: {self.stone}")
        print(f"MACHINE PARTS: {self.machineparts}")
        print(f"FISHING ROD: {self.fishingrod}")
        print(f"WEAPON: {self.weapon}")
        print(f"ARMOR: {', '.join(self.armor) if self.armor else 'None'}")
        print(f"FISH: {', '.join(self.fish) if self.fish else 'None'}\n")

    # Updates stats, handles hunger and health limits
    def update_stats(self):
        if self.hunger > 10:
            self.hunger = 10
        if self.health > self.max_health:
            self.health = self.max_health
        if self.hunger < 0:
            self.hunger = 0
            self.health -= 1
            print("You are starving! -1 HP")

# List of possible locations
LOCATIONS = ["Forest", "Lake", "Nuclear Plant", "Shack"]

# Table of fish, their roll ranges, and rarity
FISH_TABLE = [
    ("Catfish", 1, 10, "common"),
    ("Smallmouth Bass", 11, 20, "common"),
    ("Crappie", 21, 30, "common"),
    ("Bluegill", 31, 40, "common"),
    ("Largemouth Bass", 41, 45, "rare"),
    ("Trout", 46, 50, "rare"),
    ("Snail", 51, 55, "rare"),
    ("Frog", 56, 60, "rare"),
    ("Sturgeon", 61, 63, "epic"),
    ("Walleye", 64, 66, "epic"),
    ("Paddlefish", 67, 69, "epic"),
    ("Zombie Fish", 70, 71, "legendary"),
    ("Mighty Bluegill", 72, 74, "legendary"),
]

# Weapon list: (name, damage, cost)
WEAPONS = [
    ("Fists", 1, 0),
    ("Knife", 1, 5),
    ("Machete", 2, 10),
    ("Axe", 3, 20),
    ("Pistol", 4, 40),
    ("SMG", 5, 80),
    ("Shotgun", 6, 160),
    ("AR-15", 7, 200),
    ("Sniper", 8, 250),
    ("Brass Knuckles", 9, 400),
    ("Spiked Bat", 10, 600),
]

# Fishing rods: (name, luck bonus, cost)
RODS = [
    ("Stick And String", 0, 0),
    ("Common Rod", 1, 5),
    ("Sturdy Rod", 2, 20),
    ("Premium Rod", 3, 50),
    ("Deep Sea Rod", 4, 100),
    ("Jody Barrs Rod", 5, 250),
]

# Armor items: (name, type, value, cost)
ARMOR = [
    ("Medkit", "heal", 2, 10),
    ("Nurse Aimees Power Kit", "fullheal", 0, 30),
    ("Ollies Leather Coat", "maxhp", 1, 50),
    ("Tactical Kerpants", "maxhp", 2, 100),
    ("Clemuratan Helmet", "maxhp", 3, 150),
]

# Food items: (name, hunger value, cost)
FOOD = [
    ("Sage Cookies", 2, 8),
    ("Mrs Sierras Pasta", 4, 11),
    ("Chicky-fi-laa", 8, 20),
    ("Missys Cookbook", "cookbook", 0, 50),
]

# Handles character creation and customization
def character_creation(player):
    slow_print("Welcome to Zombie Pro Fisher - Byte Sized!")
    time.sleep(1)
    slow_print("\n--- Character Customization ---\n")
    # Eye color
    eye = choose("Choose eye color:", {"1": "Blue (+2 luck)", "2": "Brown (+1 damage)", "3": "Green (+2 max health)"})
    if eye == "1": player.luck += 2
    elif eye == "2": player.damage += 1
    elif eye == "3": player.max_health += 2
    # Hair color
    hair = choose("Choose hair color:", {"1": "Blonde (+2 luck)", "2": "Brown (+1 damage)", "3": "Black (+2 max health)"})
    if hair == "1": player.luck += 2
    elif hair == "2": player.damage += 1
    elif hair == "3": player.max_health += 2
    # Size
    size = choose("Choose size:", {"1": "Short (+2 luck)", "2": "Tall (+1 damage)", "3": "Medium (+2 max health)"})
    if size == "1": player.luck += 2
    elif size == "2": player.damage += 1
    elif size == "3": player.max_health += 2
    player.name = input("Now, what is your hero's name? ")
    player.health = player.max_health
    slow_print(f"\nStarting your journey now! Here are your stats:")
    player.stats()
    # Random spawn
    player.location = random.choice(LOCATIONS)
    slow_print(f"\nSPAWNING CHARACTER...")
    time.sleep(1)
    slow_print(f"You arrive at the {player.location.upper()}.")

# Handles random zombie encounters based on location
def zombie_encounter(player):
    if player.location == "Shack": return
    spawn_chance = random.randint(0, 10)
    if (spawn_chance >= 9 and player.location != "Shack") or (spawn_chance >= 5 and player.location == "Nuclear Plant"):
        zombie_hp = random.randint(5, 15)
        slow_print("\nZOMBIE ENCOUNTER!")
        while zombie_hp > 0 and player.health > 0:
            print(f"Zombie HP: {zombie_hp} | Your HP: {player.health}")
            action = choose("What do you do?", {"1": "Attack", "2": "Run away"})
            if action == "1":
                dmg = random.randint(0, 3) + player.damage
                slow_print(f"You hit the zombie for {dmg}!")
                zombie_hp -= dmg
                if zombie_hp <= 0:
                    reward = random.randint(1, 10)
                    slow_print(f"You killed the zombie! You got ${reward}.")
                    player.money += reward
                    break
                z_dmg = random.randint(0, 9)
                slow_print(f"The zombie hits you for {z_dmg}!")
                player.health -= z_dmg
            else:
                escape = random.randint(0, 20) + int(player.luck * 1.5)
                if escape >= 12:
                    slow_print("You successfully got away!")
                    break
                else:
                    slow_print("The zombie caught up to you!")
                    z_dmg = random.randint(0, 9)
                    slow_print(f"The zombie hits you for {z_dmg}!")
                    player.health -= z_dmg
        if player.health <= 0:
            slow_print("\nYOU DIED\nYou lasted {} turns. Not bad!".format(player.turns))
            return True
    return False

# Handles foraging for food and items
def forage(player):
    if player.location == "Nuclear Plant":
        slow_print("You're not sure there's anything safe to eat here...")
        return
    if player.location == "Shack":
        slow_print("Mr. Hutchinson tells you to stop snooping around in his shop.")
        return
    player.hunger -= 1
    result = random.randint(-10, 32) + int(player.luck * 1.9)
    if result <= 0:
        slow_print("You found nothing.")
    elif (result <= 10 and not player.cookbook) or (result <= 5 and player.cookbook):
        hp_loss = random.randint(1, 3)
        player.health -= hp_loss
        slow_print(f"Yuck! You ate something you shouldn't have. -{hp_loss} HP.")
    elif (result <= 20 and not player.cookbook) or (result <= 20 and player.cookbook):
        slow_print("You found some nuts and berries. +2 Hunger")
        player.hunger += 2
    elif result <= 25:
        slow_print("You're not sure what you found, but the geiger counter didn't beep - so it's probably safe. +3 Hunger.")
        player.hunger += 3
    elif result <= 30:
        slow_print("You trapped some local fauna and ate a well-cooked meal. +4 Hunger.")
        player.hunger += 4
    elif result <= 35:
        found = random.choice(WEAPONS[1:])
        slow_print(f"You found a weapon! {found[0]}")
        action = choose("Take the weapon or scrap it?", {"1": "Take", "2": "Scrap"})
        if action == "1":
            player.weapon = found[0]
            player.damage = found[1]
        else:
            parts = random.randint(0, 2)
            player.machineparts += parts
            slow_print(f"You got {parts} machine parts.")
    elif result >= 40:
        slow_print("You find a bright green triangular shape. It is crushed and deformed. On it is written '663D'. You hang onto it. It seems like good luck.")

# Handles fishing action and fish catching logic
def fishing(player):
    player.hunger -= 1
    roll = random.randint(-74, 74) + int(player.luck * 1.9)
    caught = None
    for fish, low, high, rarity in FISH_TABLE:
        if low <= roll <= high:
            caught = fish
            break
    if caught:
        slow_print(f"You caught a {caught}!")
        player.fish.append(caught)
    else:
        slow_print("You caught nothing today...")

# Handles gathering resources (wood, stone, machine parts)
def gather(player, resource):
    amount = random.randint(0, 5)
    slow_print(f"You gathered {amount} pieces of {resource}.")
    if resource == "wood":
        player.wood += amount
    elif resource == "stone":
        player.stone += amount
    elif resource == "machinery":
        player.machineparts += amount
    player.hunger -= 1

# Handles shop interactions, buying/selling/crafting
def shop(player):
    slow_print("Mr Hutchinson greets you with a warm nod and a gruffy smile.")
    while True:
        action = choose("What would you like to do?", {
            "1": "Buy weapons",
            "2": "Buy/sell fishing goods",
            "3": "Armor Shop",
            "4": "Craft",
            "5": "Sage Snack Shack",
            "6": "Goodbye"
        })
        if action == "1":
            # Weapon shop
            for i, (name, dmg, cost) in enumerate(WEAPONS[1:], 1):
                print(f"{i}) {name} (+{dmg} DMG) - ${cost}")
            print(f"{len(WEAPONS)}) Go Back")
            choice = input("> ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(WEAPONS)-1 and player.money >= WEAPONS[idx+1][2]:
                player.weapon = WEAPONS[idx+1][0]
                player.damage = WEAPONS[idx+1][1]
                player.money -= WEAPONS[idx+1][2]
                slow_print(f"You bought {player.weapon}!")
            elif choice == str(len(WEAPONS)):
                continue
            else:
                slow_print("Not enough money or invalid choice.")
        elif action == "2":
            # Fishing goods shop
            rod_options = {str(i+1): f"{rod[0]} (+{rod[1]} Luck) - ${rod[2]}" for i, rod in enumerate(RODS[1:])}
            rod_options[str(len(RODS[1:])+1)] = "Sell your fish"
            rod_options[str(len(RODS[1:])+2)] = "Goodbye"
            for k, v in rod_options.items(): print(f"{k}) {v}")
            choice = input("> ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(RODS[1:]) and player.money >= RODS[idx+1][2]:
                player.fishingrod = RODS[idx+1][0]
                player.luck = RODS[idx+1][1]
                player.money -= RODS[idx+1][2]
                slow_print(f"You bought {player.fishingrod}!")
            elif choice == str(len(RODS[1:])+1):
                # Sell fish
                rarity_values = {"common": 2, "rare": 4, "epic": 7, "legendary": 10}
                total = 0
                for fish in player.fish:
                    for f, _, _, rarity in FISH_TABLE:
                        if fish == f:
                            total += rarity_values[rarity]
                player.money += total
                slow_print(f"You sold your fish for ${total}.")
                player.fish = []
            elif choice == str(len(RODS[1:])+2):
                continue
            else:
                slow_print("Not enough money or invalid choice.")
        elif action == "3":
            # Armor shop
            for i, (name, typ, val, cost) in enumerate(ARMOR, 1):
                print(f"{i}) {name} - ${cost}")
            print(f"{len(ARMOR)+1}) Goodbye")
            choice = input("> ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(ARMOR) and player.money >= ARMOR[idx][3]:
                name, typ, val, cost = ARMOR[idx]
                if typ == "heal":
                    player.health = min(player.health + val, player.max_health)
                elif typ == "fullheal":
                    player.health = player.max_health
                elif typ == "maxhp":
                    player.max_health += val
                    player.health += val
                    player.armor.append(name)
                player.money -= cost
                slow_print(f"You bought {name}!")
            elif choice == str(len(ARMOR)+1):
                continue
            else:
                slow_print("Not enough money or invalid choice.")
        elif action == "4":
            # Crafting weapons
            print("1) Knife ($2, 5 wood, 4 stone)")
            print("2) Machete ($5, 6 wood, 10 stone)")
            print("3) Pistol ($10, 8 wood, 5 stone, 5 machine parts)")
            print("4) SMG ($20, 7 wood, 10 stone, 10 machine parts)")
            print("5) Shotgun ($80, 10 wood, 15 stone, 20 machine parts)")
            print("6) Goodbye")
            choice = input("> ").strip()
            if choice == "1" and player.money >= 2 and player.wood >= 5 and player.stone >= 4:
                player.weapon = "Knife"
                player.damage = 1
                player.money -= 2
                player.wood -= 5
                player.stone -= 4
                slow_print("You crafted a Knife!")
            elif choice == "2" and player.money >= 5 and player.wood >= 6 and player.stone >= 10:
                player.weapon = "Machete"
                player.damage = 2
                player.money -= 5
                player.wood -= 6
                player.stone -= 10
                slow_print("You crafted a Machete!")
            elif choice == "3" and player.money >= 10 and player.wood >= 8 and player.stone >= 5 and player.machineparts >= 5:
                player.weapon = "Pistol"
                player.damage = 3
                player.money -= 10
                player.wood -= 8
                player.stone -= 5
                player.machineparts -= 5
                slow_print("You crafted a Pistol!")
            elif choice == "4" and player.money >= 20 and player.wood >= 7 and player.stone >= 10 and player.machineparts >= 10:
                player.weapon = "SMG"
                player.damage = 4
                player.money -= 20
                player.wood -= 7
                player.stone -= 10
                player.machineparts -= 10
                slow_print("You crafted an SMG!")
            elif choice == "5" and player.money >= 80 and player.wood >= 10 and player.stone >= 15 and player.machineparts >= 20:
                player.weapon = "Shotgun"
                player.damage = 5
                player.money -= 80
                player.wood -= 10
                player.stone -= 15
                player.machineparts -= 20
                slow_print("You crafted a Shotgun!")
            elif choice == "6":
                continue
            else:
                slow_print("Not enough resources or invalid choice.")
        elif action == "5":
            # Food shop
            for i, (name, val, cost) in enumerate(FOOD, 1):
                print(f"{i}) {name} - ${cost}")
            print(f"{len(FOOD)+1}) Goodbye")
            choice = input("> ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(FOOD) and player.money >= FOOD[idx][2]:
                name, val, cost = FOOD[idx]
                if name == "Missys Cookbook":
                    player.cookbook = True
                else:
                    player.hunger += val
                player.money -= cost
                slow_print(f"You bought {name}!")
            elif choice == str(len(FOOD)+1):
                continue
            else:
                slow_print("Not enough money or invalid choice.")
        elif action == "6":
            break

# Main game loop
def main():
    player = Player()
    character_creation(player)
    while player.health > 0:
        player.turns += 1
        player.update_stats()
        if zombie_encounter(player):
            break
        print("\nWhat would you like to do?")
        options = {}
        # Set available actions based on location
        if player.location == "Forest":
            options = {"1": "Forage", "2": "Change location", "3": "Check stats", "4": "Gather wood", "5": "Watch birds"}
        elif player.location == "Lake":
            options = {"1": "Forage", "2": "Change location", "3": "Check stats", "4": "Go fishing", "5": "Gather rocks"}
        elif player.location == "Nuclear Plant":
            options = {"1": "Forage", "2": "Change location", "3": "Check stats", "4": "Gather machine parts", "5": "Listen to echoes"}
        elif player.location == "Shack":
            options = {"1": "Forage", "2": "Change location", "3": "Check stats", "4": "Interact with Mr. Hutchinson", "5": "Rest by the fire"}
        choice = choose("Choose an action:", options)
        if choice == "1":
            forage(player)
        elif choice == "2":
            locs = {"1": "Forest", "2": "Lake", "3": "Nuclear Plant", "4": "Shack"}
            loc_choice = choose("Where would you like to go?", locs)
            if locs[loc_choice] == player.location:
                slow_print("You can't travel to a place you're already at.")
            else:
                player.location = locs[loc_choice]
                slow_print(f"You travel to the {player.location}.")
        elif choice == "3":
            player.stats()
        elif choice == "4":
            if player.location == "Forest":
                gather(player, "wood")
            elif player.location == "Lake":
                fishing(player)
            elif player.location == "Nuclear Plant":
                gather(player, "machinery")
            elif player.location == "Shack":
                shop(player)
        elif choice == "5":
            # Location-specific events
            if player.location == "Forest":
                event = random.randint(1, 4)
                if event == 1:
                    slow_print("The birds are lively today. +1 HP.")
                    player.health = min(player.health + 1, player.max_health)
                elif event == 2:
                    slow_print("There are only a few birds today. You find peace in solitude.")
                elif event == 3:
                    slow_print("No birds today. It's quiet and eerie. -1 Damage.")
                    player.damage = max(1, player.damage - 1)
                elif event == 4:
                    slow_print("You see large birds. +1 luck, -1 Hunger.")
                    player.luck += 1
                    player.hunger -= 1
            elif player.location == "Lake":
                gather(player, "stone")
            elif player.location == "Nuclear Plant":
                event = random.randint(1, 4)
                if event == 1:
                    slow_print("You hear the humming of a machine. +1 HP.")
                    player.health = min(player.health + 1, player.max_health)
                elif event == 2:
                    slow_print("You hear water dripping in the dark corridors.")
                elif event == 3:
                    slow_print("You hear zombie screeches. -1 damage.")
                    player.damage = max(1, player.damage - 1)
                elif event == 4:
                    slow_print("You hear metal drop in the distance. +1 money.")
                    player.money += 1
            elif player.location == "Shack":
                slow_print("The fire reminds you of home.")
    slow_print("Game Over. Thanks for playing!")

# Entry point
if __name__ == "__main__":
    main()
