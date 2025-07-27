import pygame
import random
import sys

# Game constants
WIDTH, HEIGHT = 1280, 720  # 16:9 ratio
FPS = 60
TILE_SIZE = 64

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
BLUE = (70, 130, 180)
GRAY = (169, 169, 169)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)

# Locations
LOCATIONS = ["Forest", "Lake", "Nuclear Plant", "Shack"]
LOCATION_COLORS = {"Forest": GREEN, "Lake": BLUE, "Nuclear Plant": GRAY, "Shack": YELLOW}

# Player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
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
        self.name = "Hero"
        self.location = "Forest"
        self.turns = 0

    def update_stats(self):
        if self.hunger > 10:
            self.hunger = 10
        if self.health > self.max_health:
            self.health = self.max_health
        if self.hunger < 0:
            self.hunger = 0
            self.health -= 1

# Main game class
class Game:
    def draw_message(self):
        if self.animated_message:
            txt = self.font.render(self.animated_message, True, YELLOW)
            txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            self.screen.blit(txt, txt_rect)
    def draw_options(self):
        options = [
            "1 Forage",
            "2 Change Location",
            "3 Location Action",
            "4 Special Event"
        ]
        self.button_rects = []
        button_width = 320
        button_height = 50
        gap = 8
        left_padding = 10
        bottom_padding = 10
        total_height = len(options) * (button_height + gap) - gap
        start_y = HEIGHT - total_height - bottom_padding
        mouse_pos = pygame.mouse.get_pos()
        # If location menu is open, disable other buttons
        for i, opt in enumerate(options):
            x = left_padding
            y = start_y + i * (button_height + gap)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.button_rects.append(rect)
            # Disable other buttons if location menu is open
            if getattr(self, 'location_menu_open', False):
                if i != 1:
                    color = (80, 80, 80)  # Disabled
                else:
                    color = GRAY
            else:
                color = GRAY
                if hasattr(self, 'clicked_button') and self.clicked_button == i:
                    color = (120, 120, 120)
                elif rect.collidepoint(mouse_pos):
                    color = (200, 200, 200)
            pygame.draw.rect(self.screen, color, rect, border_radius=10)
            txt = self.font.render(opt, True, BLACK)
            txt_x = rect.x + 16
            txt_y = rect.y + (button_height - txt.get_height()) // 2
            self.screen.blit(txt, (txt_x, txt_y))

        # Draw location selection menu if open
        if getattr(self, 'location_menu_open', False):
            current_loc = self.player.location
            locs = [loc for loc in LOCATIONS if loc != current_loc]
            locs_with_exit = locs + ["Cancel"]
            self.location_button_rects = []
            loc_button_width = 260
            loc_button_height = 50
            loc_gap = gap  # Use same gap as main menu buttons
            # Set horizontal distance between button sets to match gap
            loc_start_x = left_padding + button_width + gap
            loc_start_y = start_y + button_height + gap
            num_buttons = len(locs_with_exit)
            # Move all buttons down 2 slots
            for i, loc in enumerate(locs_with_exit):
                x = loc_start_x
                y = loc_start_y + (i + 2 - (num_buttons - 1)) * (loc_button_height + loc_gap)
                rect = pygame.Rect(x, y, loc_button_width, loc_button_height)
                self.location_button_rects.append(rect)
                color = LOCATION_COLORS.get(loc, GRAY)
                if hasattr(self, 'clicked_location_button') and self.clicked_location_button == i:
                    color = (min(color[0]+40,255), min(color[1]+40,255), min(color[2]+40,255))
                elif rect.collidepoint(mouse_pos):
                    color = (min(color[0]+80,255), min(color[1]+80,255), min(color[2]+80,255))
                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                # Add number in front of location name (no colon)
                if loc == "Cancel":
                    txt = self.font.render(f"{i+1} Cancel", True, BLACK)
                else:
                    txt = self.font.render(f"{i+1} {loc}", True, BLACK)
                txt_x = rect.x + 16
                txt_y = rect.y + (loc_button_height - txt.get_height()) // 2
                self.screen.blit(txt, (txt_x, txt_y))
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ZPF: Ground Zero")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Jersey10-Regular.ttf", 32)
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.running = True
        self.state = "main"  # main, shop, event, etc.
        self.message = ""
        # Typewriter animation variables
        self.animated_message = ""
        self.message_index = 0
        self.message_timer = 0
        self.message_speed = 2  # frames per character (lower is faster)
        # Typewriter for stats
        self.stats_animated = ["" for _ in range(14)]
        self.stats_index = [0 for _ in range(14)]
        self.stats_timer = [0 for _ in range(14)]
        self.stats_speed = 2
        # Typewriter for options
        self.options_animated = ["" for _ in range(4)]
        self.options_index = [0 for _ in range(4)]
        self.options_timer = [0 for _ in range(4)]
        self.options_speed = 2

    def draw_stats(self):
        stats = [
            f"NAME: {self.player.name}",
            f"HEALTH: {self.player.health}/{self.player.max_health}",
            f"DAMAGE: {self.player.damage}",
            f"LUCK: {self.player.luck}",
            f"HUNGER: {self.player.hunger}",
            f"MONEY: {self.player.money}",
            f"WOOD: {self.player.wood}",
            f"STONE: {self.player.stone}",
            f"MACHINE PARTS: {self.player.machineparts}",
            f"FISHING ROD: {self.player.fishingrod}",
            f"WEAPON: {self.player.weapon}",
            f"ARMOR: {', '.join(self.player.armor) if self.player.armor else 'None'}",
            f"FISH: {', '.join(self.player.fish) if self.player.fish else 'None'}"
        ]
        for i, stat in enumerate(stats):
            txt = self.font.render(self.stats_animated[i], True, WHITE)
            self.screen.blit(txt, (10, 10 + i * 28))

    # Removed old text-based draw_options. Only button-based draw_options is used.
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # If location menu is open, allow number keys to select location
                if getattr(self, 'location_menu_open', False):
                    # Only allow 1,2,3 keys for location selection
                    for i in range(3):
                        if event.key in [getattr(pygame, f'K_{i+1}'), getattr(pygame, f'K_KP{i+1}')]:
                            self.change_location_direct(i)
                            self.location_menu_open = False
                            self.clicked_location_button = None
                            break
                    continue
                elif event.key in [pygame.K_1, pygame.K_KP1]:
                    self.clicked_button = 0
                    self.set_message(self.do_action(1))
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    self.clicked_button = 1
                    # Open location menu instead of changing location immediately
                    self.location_menu_open = True
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    self.clicked_button = 2
                    self.set_message(self.do_action(3))
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    self.clicked_button = 3
                    self.set_message(self.do_action(4))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # If location menu is open, only allow location buttons
                if getattr(self, 'location_menu_open', False):
                    if hasattr(self, 'location_button_rects'):
                        for i, rect in enumerate(self.location_button_rects):
                            if rect.collidepoint(mouse_pos):
                                self.clicked_location_button = i
                                break
                    return
                if hasattr(self, 'button_rects'):
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            self.clicked_button = i
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_pos = event.pos
                # If location menu is open, handle location selection
                if getattr(self, 'location_menu_open', False):
                    clicked = False
                    if hasattr(self, 'location_button_rects'):
                        for i, rect in enumerate(self.location_button_rects):
                            if rect.collidepoint(mouse_pos):
                                # If Cancel button is clicked (always last)
                                current_loc = self.player.location
                                locs = [loc for loc in LOCATIONS if loc != current_loc]
                                if i == len(locs):
                                    self.location_menu_open = False
                                    self.clicked_location_button = None
                                    clicked = True
                                    break
                                else:
                                    self.change_location_direct(i)
                                    self.location_menu_open = False
                                    self.clicked_location_button = None
                                    clicked = True
                                    break
                    # If clicked outside location buttons, close menu
                    if not clicked:
                        self.location_menu_open = False
                        self.clicked_location_button = None
                    return
                if hasattr(self, 'button_rects'):
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            self.set_message(self.do_action(i + 1))
                self.clicked_button = None
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_1, pygame.K_KP1, pygame.K_2, pygame.K_KP2, pygame.K_3, pygame.K_KP3, pygame.K_4, pygame.K_KP4]:
                    self.clicked_button = None

    def set_message(self, msg):
        self.message = msg
        self.animated_message = ""
        self.message_index = 0
        self.message_timer = 0

    def do_action(self, action):
        loc = self.player.location
        if action == 1:
            return self.forage()
        elif action == 2:
            return self.change_location()
        elif action == 3:
            if loc == "Forest":
                return self.gather("wood")
            elif loc == "Lake":
                return self.fishing()
            elif loc == "Nuclear Plant":
                return self.gather("machinery")
            elif loc == "Shack":
                return self.shop()
        elif action == 4:
            return self.special_event()
        return "Invalid action."

    def forage(self):
        self.player.hunger -= 1
        result = random.randint(-10, 32) + int(self.player.luck * 1.9)
        if result <= 0:
            return "You found nothing."
        elif result <= 10:
            hp_loss = random.randint(1, 3)
            self.player.health -= hp_loss
            return f"Yuck! You ate something you shouldn't have. -{hp_loss} HP."
        elif result <= 20:
            self.player.hunger += 2
            return "You found some nuts and berries. +2 Hunger"
        elif result <= 25:
            self.player.hunger += 3
            return "You found something safe. +3 Hunger."
        elif result <= 30:
            self.player.hunger += 4
            return "You ate a well-cooked meal. +4 Hunger."
        elif result <= 35:
            self.player.weapon = "Knife"
            self.player.damage = 1
            return "You found a Knife!"
        elif result >= 40:
            return "You find a bright green triangular shape. It seems like good luck."
        return "Forage event."

    def change_location(self):
        # Open location menu instead of changing location immediately
        self.location_menu_open = True
        return "Choose a location to travel to."

    def change_location_direct(self, idx):
        # idx is the index in the filtered location list
        current_loc = self.player.location
        locs = [loc for loc in LOCATIONS if loc != current_loc]
        self.player.location = locs[idx]
        self.set_message(f"You travel to the {self.player.location}.")

    def gather(self, resource):
        amount = random.randint(0, 5)
        if resource == "wood":
            self.player.wood += amount
        elif resource == "stone":
            self.player.stone += amount
        elif resource == "machinery":
            self.player.machineparts += amount
        self.player.hunger -= 1
        return f"You gathered {amount} pieces of {resource}."

    def fishing(self):
        self.player.hunger -= 1
        roll = random.randint(-74, 74) + int(self.player.luck * 1.9)
        fish_list = ["Catfish", "Bass", "Crappie", "Bluegill", "Trout", "Snail", "Frog", "Sturgeon", "Walleye", "Paddlefish", "Zombie Fish", "Mighty Bluegill"]
        caught = random.choice(fish_list) if roll > 0 else None
        if caught:
            self.player.fish.append(caught)
            return f"You caught a {caught}!"
        else:
            return "You caught nothing today..."

    def shop(self):
        self.player.money -= 5
        self.player.armor.append("Medkit")
        self.player.health = min(self.player.health + 2, self.player.max_health)
        return "You bought a Medkit! +2 HP."

    def special_event(self):
        loc = self.player.location
        if loc == "Forest":
            self.player.health = min(self.player.health + 1, self.player.max_health)
            return "The birds are lively today. +1 HP."
        elif loc == "Lake":
            self.player.stone += 1
            return "You gathered a stone."
        elif loc == "Nuclear Plant":
            self.player.money += 1
            return "You hear metal drop in the distance. +1 money."
        elif loc == "Shack":
            return "The fire reminds you of home."
        return "Special event."

    def draw_death_screen(self):
        self.screen.fill(BLACK)
        death_text = self.font.render("You have died!", True, RED)
        sub_text = self.font.render("Press ESC to exit.", True, WHITE)
        text_rect = death_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        self.screen.blit(death_text, text_rect)
        self.screen.blit(sub_text, sub_rect)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.player.update_stats()

            # Typewriter animation update for message
            if self.message:
                if self.message_index < len(self.message):
                    self.message_timer += 1
                    if self.message_timer >= self.message_speed:
                        self.message_index += 1
                        self.message_timer = 0
                    self.animated_message = self.message[:self.message_index]
                else:
                    self.animated_message = self.message
            else:
                self.animated_message = ""

            # Typewriter animation for stats
            stats = [
                f"NAME: {self.player.name}",
                f"HEALTH: {self.player.health}/{self.player.max_health}",
                f"DAMAGE: {self.player.damage}",
                f"LUCK: {self.player.luck}",
                f"HUNGER: {self.player.hunger}",
                f"MONEY: {self.player.money}",
                f"WOOD: {self.player.wood}",
                f"STONE: {self.player.stone}",
                f"MACHINE PARTS: {self.player.machineparts}",
                f"FISHING ROD: {self.player.fishingrod}",
                f"WEAPON: {self.player.weapon}",
                f"ARMOR: {', '.join(self.player.armor) if self.player.armor else 'None'}",
                f"FISH: {', '.join(self.player.fish) if self.player.fish else 'None'}"
            ]
            for i, stat in enumerate(stats):
                if self.stats_index[i] < len(stat):
                    self.stats_timer[i] += 1
                    if self.stats_timer[i] >= self.stats_speed:
                        self.stats_index[i] += 1
                        self.stats_timer[i] = 0
                    self.stats_animated[i] = stat[:self.stats_index[i]]
                else:
                    self.stats_animated[i] = stat

            # Typewriter animation for options
            options = [
                "1: Forage",
                "2: Change Location",
                "3: Location Action",
                "4: Special Event"
            ]
            for i, opt in enumerate(options):
                if self.options_index[i] < len(opt):
                    self.options_timer[i] += 1
                    if self.options_timer[i] >= self.options_speed:
                        self.options_index[i] += 1
                        self.options_timer[i] = 0
                    self.options_animated[i] = opt[:self.options_index[i]]
                else:
                    self.options_animated[i] = opt

            if self.player.health <= 0:
                self.draw_death_screen()
                pygame.display.flip()
                pygame.quit()
                sys.exit()
            else:
                self.screen.fill(BLACK)
                self.draw_location()
                self.all_sprites.draw(self.screen)
                self.draw_stats()
                self.draw_options()
                self.draw_message()
                pygame.display.flip()

    def draw_location(self):
        # Draw the current location name and background color
        color = LOCATION_COLORS.get(self.player.location, GRAY)
        pygame.draw.rect(self.screen, color, (0, 0, WIDTH, HEIGHT // 4))
        loc_text = self.font.render(f"Location: {self.player.location}", True, BLACK)
        self.screen.blit(loc_text, (WIDTH // 2 - loc_text.get_width() // 2, 20))

if __name__ == "__main__":
    game = Game()
    game.run()
