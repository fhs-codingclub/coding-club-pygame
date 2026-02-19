# this is VIBE CODED!! please note that 

import pygame
import random
import os

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Global screen variable (will be set by init or run_battle)
screen = None

# Colors (Earthbound-inspired palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 170)
LIGHT_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
DARK_BLUE = (20, 20, 80)

# Fonts (initialized later after pygame.init())
font = None
small_font = None

# Placeholder enemy image path - change this to your image!
ENEMY_IMAGE_PATH = "./img/ryan.jpg"


def init_fonts():
    """Initialize fonts after pygame is ready."""
    global font, small_font
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)


class Combatant:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.defending = False
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - (self.defense * 2 if self.defending else self.defense))
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def is_alive(self):
        return self.hp > 0


class Player(Combatant):
    def __init__(self):
        super().__init__("Hero", max_hp=100, attack=15, defense=5)
        self.items = {"Hamburger": 3, "Lifeup": 1}
    
    def use_item(self, item_name):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            if item_name == "Hamburger":
                heal = 30
            elif item_name == "Lifeup":
                heal = 60
            else:
                heal = 20
            self.hp = min(self.max_hp, self.hp + heal)
            return heal
        return 0


class Enemy(Combatant):
    def __init__(self, image_path):
        super().__init__("Enemy", max_hp=80, attack=12, defense=3)
        self.image = None
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (150, 150))
        else:
            # Create a placeholder surface if image doesn't exist
            self.image = pygame.Surface((150, 150))
            self.image.fill(RED)
            text = small_font.render("ENEMY", True, WHITE)
            self.image.blit(text, (40, 65))


class BattleSystem:
    def __init__(self):
        self.player = Player()
        self.enemy = Enemy(ENEMY_IMAGE_PATH)
        self.state = "menu"  # menu, items, animating, enemy_turn, victory, defeat, run_away
        self.menu_options = ["Attack", "Items", "Defend", "Run Away"]
        self.selected_option = 0
        self.item_options = list(self.player.items.keys())
        self.selected_item = 0
        self.message = ""
        self.message_timer = 0
        self.clock = pygame.time.Clock()
        
        # Animation variables
        self.shake_timer = 0
        self.enemy_offset = [0, 0]
    
    def draw_window(self, rect, border_color=LIGHT_BLUE):
        """Draw an Earthbound-style window"""
        pygame.draw.rect(screen, DARK_BLUE, rect)
        pygame.draw.rect(screen, border_color, rect, 4)
        # Inner border
        inner_rect = (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8)
        pygame.draw.rect(screen, BLACK, inner_rect, 2)
    
    def draw_hp_bar(self, x, y, current_hp, max_hp, width=200):
        """Draw a rolling HP counter style bar"""
        ratio = current_hp / max_hp
        # Background
        pygame.draw.rect(screen, BLACK, (x, y, width, 20))
        # HP bar
        color = GREEN if ratio > 0.5 else YELLOW if ratio > 0.25 else RED
        pygame.draw.rect(screen, color, (x, y, int(width * ratio), 20))
        # Border
        pygame.draw.rect(screen, WHITE, (x, y, width, 20), 2)
        # Text
        hp_text = small_font.render(f"{current_hp}/{max_hp}", True, WHITE)
        screen.blit(hp_text, (x + width + 10, y))
    
    def draw_battle_scene(self):
        """Draw the main battle scene"""
        # Psychedelic background (simple version)
        screen.fill(DARK_BLUE)
        
        # Draw swirling background pattern
        time = pygame.time.get_ticks() / 1000
        for i in range(0, SCREEN_WIDTH, 40):
            for j in range(0, 240, 40):
                color_val = int((i + j + time * 50) % 100) + 20
                pygame.draw.circle(screen, (color_val // 2, color_val // 2, color_val), 
                                 (i + 20, j + 20), 15)
        
        # Draw enemy with shake effect
        enemy_x = SCREEN_WIDTH // 2 - 75 + self.enemy_offset[0]
        enemy_y = 50 + self.enemy_offset[1]
        screen.blit(self.enemy.image, (enemy_x, enemy_y))
        
        # Enemy HP bar
        self.draw_hp_bar(SCREEN_WIDTH // 2 - 100, 210, self.enemy.hp, self.enemy.max_hp)
        enemy_name = small_font.render(self.enemy.name, True, WHITE)
        screen.blit(enemy_name, (SCREEN_WIDTH // 2 - 30, 190))
    
    def draw_menu(self):
        """Draw the battle menu to match wood feel and layout from image, fit screen"""
        # Colors for wood theme
        wood_base = (120, 80, 40)
        wood_dark = (80, 50, 20)
        wood_light = (160, 120, 60)
        wood_circle = (140, 100, 60)
        wood_grid = (100, 70, 40)
        # Panel height
        panel_height = 180
        # Draw wood bottom bar
        pygame.draw.rect(screen, wood_base, (0, SCREEN_HEIGHT - panel_height, SCREEN_WIDTH, panel_height))
        pygame.draw.rect(screen, wood_dark, (0, SCREEN_HEIGHT - panel_height, SCREEN_WIDTH, panel_height), 8)

        # Draw wood circle in center bottom
        circle_radius = 110
        circle_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - panel_height // 2)
        pygame.draw.circle(screen, wood_circle, circle_center, circle_radius)
        pygame.draw.circle(screen, wood_dark, circle_center, circle_radius, 8)
        # Draw concentric rings for wood effect
        for r in range(10, circle_radius, 15):
            pygame.draw.circle(screen, wood_grid, circle_center, r, 2)

        # ...removed grid drawing for cleaner wood UI...


        # Button layout values
        button_w = 180
        button_h = 40
        button_gap = 10
        left_x = 40
        left_y_start = SCREEN_HEIGHT - panel_height + 20
        for i, option in enumerate(self.menu_options):
            y = left_y_start + i * (button_h + button_gap)
            color = wood_light if self.state == "menu" and i == self.selected_option else wood_base
            pygame.draw.rect(screen, color, (left_x, y, button_w, button_h), border_radius=12)
            pygame.draw.rect(screen, wood_dark, (left_x, y, button_w, button_h), 2, border_radius=12)
            text = small_font.render(option, True, WHITE)
            text_rect = text.get_rect(center=(left_x + button_w // 2, y + button_h // 2))
            screen.blit(text, text_rect)

        # Draw inventory/items as wood-themed buttons on right
        right_x = SCREEN_WIDTH - button_w - 40
        right_y_start = SCREEN_HEIGHT - panel_height + 20
        if self.state == "items":
            if self.item_options:
                for i, item in enumerate(self.item_options):
                    y = right_y_start + i * (button_h + button_gap)
                    color = wood_light if i == self.selected_item else wood_base
                    pygame.draw.rect(screen, color, (right_x, y, button_w, button_h), border_radius=12)
                    pygame.draw.rect(screen, wood_dark, (right_x, y, button_w, button_h), 2, border_radius=12)
                    text = small_font.render(f"{item} x{self.player.items[item]}", True, WHITE)
                    text_rect = text.get_rect(center=(right_x + button_w // 2, y + button_h // 2))
                    screen.blit(text, text_rect)
            else:
                y = right_y_start
                pygame.draw.rect(screen, wood_base, (right_x, y, button_w, button_h), border_radius=12)
                pygame.draw.rect(screen, wood_dark, (right_x, y, button_w, button_h), 2, border_radius=12)
                text = small_font.render("No items!", True, WHITE)
                text_rect = text.get_rect(center=(right_x + button_w // 2, y + button_h // 2))
                screen.blit(text, text_rect)

        # Draw player stats above right panel
        stats_y = SCREEN_HEIGHT - panel_height + 10
        name_text = small_font.render(self.player.name, True, WHITE)
        screen.blit(name_text, (right_x, stats_y))
        hp_text = small_font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, GREEN if self.player.hp > 30 else RED)
        screen.blit(hp_text, (right_x, stats_y + 25))
        if self.player.defending:
            def_text = small_font.render("DEFENDING", True, wood_light)
            screen.blit(def_text, (right_x + 100, stats_y + 25))

        # Draw message or default text in center circle
        if self.message:
            msg_text = font.render(self.message, True, WHITE)
            text_rect = msg_text.get_rect(center=circle_center)
            screen.blit(msg_text, text_rect)
        else:
            msg_text = font.render("What will you do?", True, WHITE)
            text_rect = msg_text.get_rect(center=circle_center)
            screen.blit(msg_text, text_rect)
    
    def handle_input(self, event):
        """Handle keyboard input"""
        if event.type != pygame.KEYDOWN:
            return
        
        if self.state == "menu":
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 4
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 4
            elif event.key == pygame.K_LEFT:
                self.selected_option = (self.selected_option - 2) % 4
            elif event.key == pygame.K_RIGHT:
                self.selected_option = (self.selected_option + 2) % 4
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                self.execute_action(self.menu_options[self.selected_option])
        
        elif self.state == "items":
            if event.key == pygame.K_UP:
                self.selected_item = max(0, self.selected_item - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_item = min(len(self.item_options) - 1, self.selected_item + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_z):
                if self.item_options:
                    self.use_item(self.item_options[self.selected_item])
            elif event.key in (pygame.K_ESCAPE, pygame.K_x):
                self.state = "menu"
        
        elif self.state in ("victory", "defeat", "run_away"):
            if event.key in (pygame.K_RETURN, pygame.K_z):
                self.reset_battle()
    
    def execute_action(self, action):
        """Execute the selected action"""
        self.player.defending = False
        
        if action == "Attack":
            damage = self.player.attack + random.randint(-3, 5)
            actual_damage = self.enemy.take_damage(damage)
            self.message = f"You attack! {actual_damage} damage!"
            self.shake_timer = 20
            
            if not self.enemy.is_alive():
                self.state = "victory"
                self.message = "YOU WIN!"
            else:
                self.state = "animating"
                self.message_timer = 60
        
        elif action == "Items":
            self.item_options = [k for k, v in self.player.items.items() if v > 0]
            if self.item_options:
                self.state = "items"
                self.selected_item = 0
            else:
                self.message = "No items left!"
                self.message_timer = 60
        
        elif action == "Defend":
            self.player.defending = True
            self.message = "You brace yourself!"
            self.state = "animating"
            self.message_timer = 60
        
        elif action == "Run Away":
            if random.random() < 0.5:
                self.state = "run_away"
                self.message = "Got away safely!"
            else:
                self.message = "Can't escape!"
                self.state = "animating"
                self.message_timer = 60
    
    def use_item(self, item_name):
        """Use an item"""
        heal = self.player.use_item(item_name)
        if heal > 0:
            self.message = f"Used {item_name}! Recovered {heal} HP!"
            self.item_options = [k for k, v in self.player.items.items() if v > 0]
            self.state = "animating"
            self.message_timer = 60
    
    def enemy_turn(self):
        """Execute enemy's turn"""
        damage = self.enemy.attack + random.randint(-2, 4)
        actual_damage = self.player.take_damage(damage)
        self.message = f"{self.enemy.name} attacks! {actual_damage} damage!"
        
        if not self.player.is_alive():
            self.state = "defeat"
            self.message = "YOU LOST..."
        else:
            self.state = "enemy_animating"
            self.message_timer = 60
    
    def update(self):
        """Update battle state"""
        # Handle shake animation
        if self.shake_timer > 0:
            self.shake_timer -= 1
            self.enemy_offset = [random.randint(-5, 5), random.randint(-3, 3)]
        else:
            self.enemy_offset = [0, 0]
        
        # Handle message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                if self.state == "animating":
                    if self.enemy.is_alive() and self.player.is_alive():
                        self.state = "enemy_turn"
                        self.enemy_turn()
                    else:
                        self.state = "menu"
                        self.message = ""
                elif self.state == "enemy_animating":
                    self.player.defending = False
                    self.state = "menu"
                    self.message = ""
    
    def reset_battle(self):
        """Reset the battle"""
        self.player = Player()
        self.enemy = Enemy(ENEMY_IMAGE_PATH)
        self.state = "menu"
        self.selected_option = 0
        self.message = ""
        self.message_timer = 0
    
    def draw(self):
        """Draw everything"""
        self.draw_battle_scene()
        self.draw_menu()
        
        # Draw victory/defeat overlay
        if self.state in ("victory", "defeat", "run_away"):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(150)
            screen.blit(overlay, (0, 0))
            
            text = font.render(self.message, True, YELLOW if self.state == "victory" else WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            
            continue_text = small_font.render("Press Z to continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(continue_text, continue_rect)
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)
            
            self.update()
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()


def run_battle(game_screen):
    """Run the battle system with the provided screen."""
    global screen
    screen = game_screen
    init_fonts()
    pygame.display.set_caption("yes we're fighting ryan gosling")
    battle = BattleSystem()
    battle.run()


# Run the battle!
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("yes we're fighting ryan gosling")
    init_fonts()
    battle = BattleSystem()
    battle.run()
    pygame.quit()
