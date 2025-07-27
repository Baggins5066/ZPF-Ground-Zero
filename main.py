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
    def draw_options(self):
        options = [
            "1: Forage",
            "2: Change Location",
            "3: Show Stats",
            "4: Location Action",
            "5: Special Event"
        ]
        for i, opt in enumerate(options):
            txt = self.font.render(opt, True, WHITE)
            self.screen.blit(txt, (10, HEIGHT - 150 + i * 28))
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Pro Fisher - 2D")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Jersey10-Regular.ttf", 32)
        self.player = Player()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.running = True
        self.state = "main"  # main, shop, event, etc.
        self.message = ""

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
            txt = self.font.render(stat, True, WHITE)
            self.screen.blit(txt, (10, 10 + i * 28))

    def draw_location(self):
        color = LOCATION_COLORS.get(self.player.location, BLACK)
        pygame.draw.rect(self.screen, color, (0, HEIGHT//2, WIDTH, HEIGHT//2))
        # Draw current location centered at the top
        txt = self.font.render(f"Location: {self.player.location}", True, YELLOW)
        text_rect = txt.get_rect(center=(WIDTH // 2, 30))
        self.screen.blit(txt, text_rect)

    def draw_message(self):
        if self.message:
            txt = self.font.render(self.message, True, YELLOW)
            self.screen.blit(txt, (WIDTH//2 - 200, HEIGHT - 40))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.message = self.do_action(1)
                elif event.key == pygame.K_2:
                    self.message = self.do_action(2)
                elif event.key == pygame.K_3:
                    self.message = self.do_action(3)
                elif event.key == pygame.K_4:
                    self.message = self.do_action(4)
                elif event.key == pygame.K_5:
                    self.message = self.do_action(5)

    def do_action(self, action):
        loc = self.player.location
        if action == 1:
            return self.forage()
        elif action == 2:
            return self.change_location()
        elif action == 3:
            return "Stats shown above."
        elif action == 4:
            if loc == "Forest":
                return self.gather("wood")
            elif loc == "Lake":
                return self.fishing()
            elif loc == "Nuclear Plant":
                return self.gather("machinery")
            elif loc == "Shack":
                return self.shop()
        elif action == 5:
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
        idx = LOCATIONS.index(self.player.location)
        idx = (idx + 1) % len(LOCATIONS)
        self.player.location = LOCATIONS[idx]
        return f"You travel to the {self.player.location}."

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
            if self.player.health <= 0:
                self.draw_death_screen()
            else:
                self.screen.fill(BLACK)
                self.draw_location()
                self.all_sprites.draw(self.screen)
                self.draw_stats()
                self.draw_options()
                self.draw_message()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
