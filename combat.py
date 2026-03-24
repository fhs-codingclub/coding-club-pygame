import pygame
import random
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))

from py import inventory
from Enemy import Enemy 
from moves import MOVES  
from dice import roll_attack, calculate_damage, roll_dice
<<<<<<< HEAD
from moves import ENEMY_MOVES
=======
from loader import blit_letterboxed
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

# Logical resolution — game always renders at this size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
<<<<<<< HEAD
=======

# logical = the 640x480 surface everything draws to
# screen  = the real window (may be larger)
logical = None
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
screen = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 170)
LIGHT_BLUE = (100, 100, 255)
YELLOW = (255, 255, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
DARK_BLUE = (20, 20, 80)

font = None
small_font = None

def init_fonts():
    global font, small_font
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)

<<<<<<< HEAD
=======

class Combatant:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.defending = False

    def take_damage(self, damage):
        actual_damage = max(
            1,
            damage - (self.defense * 2 if self.defending else self.defense)
        )
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.hp > 0


class Player(Combatant):
    def __init__(self):
        invent = inventory.InventorySystem()
        super().__init__("Hero", invent.maxhealth, invent.attack, invent.defense)
        self.items = {"Hamburger": 3, "Lifeup": 1}
        self.hp = invent.health

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
        super().__init__("Enemy", 80, 12, 3)
        self.image = None
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (150, 150))
        else:
            self.image = pygame.Surface((150, 150))
            self.image.fill(RED)
            text = small_font.render("ENEMY", True, WHITE)
            self.image.blit(text, (40, 65))


>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
class BattleSystem:
    def __init__(self, player, inventory_sys, enemy_name):
        self.player = player
        self.player_inventory = inventory_sys
        self.enemy = Enemy(enemy_name)

        self.state = "menu"
        self.menu_options = ["Attack", "Items", "Stances", "Run Away"]
        self.stance_options = ["Neutral", "Aggressive", "Iron", "Berserk"]
        self.selected_stance = 0
        self.selected_option = 0

        self.item_options = [item[0] for item in self.player_inventory.inventory if item != 'air']
        self.selected_item = 0

        self.message = ""
        self.message_timer = 0
        self.clock = pygame.time.Clock()
        self.shake_timer = 0
        self.enemy_offset = [0, 0]

<<<<<<< HEAD
    def draw_hp_bar(self, x, y, current_hp, max_hp, width=200):
        ratio = max(0, min(current_hp / max_hp, 1))
        pygame.draw.rect(screen, BLACK, (x, y, width, 20))
        color = GREEN if ratio > 0.5 else YELLOW if ratio > 0.25 else RED
        pygame.draw.rect(screen, color, (x, y, int(width * ratio), 20))
        pygame.draw.rect(screen, WHITE, (x, y, width, 20), 2)
=======
    def draw_window(self, rect, border_color=LIGHT_BLUE):
        pygame.draw.rect(logical, DARK_BLUE, rect)
        pygame.draw.rect(logical, border_color, rect, 4)
        inner_rect = (rect[0] + 4, rect[1] + 4, rect[2] - 8, rect[3] - 8)
        pygame.draw.rect(logical, BLACK, inner_rect, 2)

    def draw_hp_bar(self, x, y, current_hp, max_hp, width=200):
        ratio = current_hp / max_hp
        pygame.draw.rect(logical, BLACK, (x, y, width, 20))
        color = GREEN if ratio > 0.5 else YELLOW if ratio > 0.25 else RED
        pygame.draw.rect(logical, color, (x, y, int(width * ratio), 20))
        pygame.draw.rect(logical, WHITE, (x, y, width, 20), 2)
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
        hp_text = small_font.render(f"{current_hp}/{max_hp}", True, WHITE)
        logical.blit(hp_text, (x + width + 10, y))

    def draw_battle_scene(self):
<<<<<<< HEAD
        screen.fill(DARK_BLUE)
=======
        logical.fill(DARK_BLUE)

>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
        time = pygame.time.get_ticks() / 1000
        for i in range(0, SCREEN_WIDTH, 40):
            for j in range(0, 240, 40):
                color_val = int((i + j + time * 50) % 100) + 20
<<<<<<< HEAD
                pygame.draw.circle(screen, (color_val // 2, color_val // 2, color_val), (i + 20, j + 20), 15)

        enemy_x = SCREEN_WIDTH // 2 - 75 + self.enemy_offset[0]
        enemy_y = 50 + self.enemy_offset[1]
        
        # Draw Enemy Image (or placeholder if image missing)
        screen.blit(self.enemy.image, (enemy_x, enemy_y))

        self.draw_hp_bar(SCREEN_WIDTH // 2 - 100, 210, self.enemy.hp, self.enemy.max_hp)
        enemy_name_text = small_font.render(self.enemy.name, True, WHITE)
        screen.blit(enemy_name_text, (SCREEN_WIDTH // 2 - 30, 190))
=======
                pygame.draw.circle(
                    logical,
                    (color_val // 2, color_val // 2, color_val),
                    (i + 20, j + 20),
                    15
                )

        enemy_x = SCREEN_WIDTH // 2 - 75 + self.enemy_offset[0]
        enemy_y = 50 + self.enemy_offset[1]
        logical.blit(self.enemy.image, (enemy_x, enemy_y))

        self.draw_hp_bar(SCREEN_WIDTH // 2 - 100, 210,
                         self.enemy.hp, self.enemy.max_hp)

        enemy_name = small_font.render(self.enemy.name, True, WHITE)
        logical.blit(enemy_name, (SCREEN_WIDTH // 2 - 30, 190))
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

    def draw_menu(self):
        wood_base = (120, 80, 40)
        wood_dark = (80, 50, 20)
        wood_light = (160, 120, 60)
        wood_circle = (140, 100, 60)
        wood_grid = (100, 70, 40)

        panel_height = 180
        panel_top = SCREEN_HEIGHT - panel_height

<<<<<<< HEAD
        pygame.draw.rect(screen, wood_base, (0, panel_top, SCREEN_WIDTH, panel_height))
        pygame.draw.rect(screen, wood_dark, (0, panel_top, SCREEN_WIDTH, panel_height), 8)
=======
        pygame.draw.rect(logical, wood_base, (0, panel_top, SCREEN_WIDTH, panel_height))
        pygame.draw.rect(logical, wood_dark, (0, panel_top, SCREEN_WIDTH, panel_height), 8)
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

        circle_radius = 110
        circle_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - panel_height // 2)

        pygame.draw.circle(logical, wood_circle, circle_center, circle_radius)
        pygame.draw.circle(logical, wood_dark, circle_center, circle_radius, 8)

        for r in range(10, circle_radius, 15):
            pygame.draw.circle(logical, wood_grid, circle_center, r, 2)

        padding = 10
        left_x = padding
        left_width = max((circle_center[0] - circle_radius) - padding * 2, 10)
        right_x = circle_center[0] + circle_radius + padding
        right_width = max(SCREEN_WIDTH - right_x - padding, 10)

        n = len(self.menu_options)
        available_h = panel_height - 20
<<<<<<< HEAD
        button_h = min(45, (available_h - (8 * (n - 1))) // n)
        start_y = panel_top + (panel_height - (button_h * n + 8 * (n - 1))) // 2

        # Draw Menu Buttons
        for i, option in enumerate(self.menu_options):
            y = start_y + i * (button_h + 8)
            color = wood_light if (self.state == "menu" and i == self.selected_option) else wood_base
            pygame.draw.rect(screen, color, (left_x, y, left_width, button_h), border_radius=10)
            pygame.draw.rect(screen, wood_dark, (left_x, y, left_width, button_h), 2, border_radius=10)
            text = small_font.render(option, True, WHITE)
            screen.blit(text, text.get_rect(center=(left_x + left_width // 2, y + button_h // 2)))

        # Draw Items or Stats
        if self.state == "items":
            if self.item_options:
                for i, item in enumerate(self.item_options):
                    y = start_y + i * (button_h + 8)
                    color = wood_light if i == self.selected_item else wood_base
                    pygame.draw.rect(screen, color, (right_x, y, right_width, button_h), border_radius=10)
                    pygame.draw.rect(screen, wood_dark, (right_x, y, right_width, button_h), 2, border_radius=10)
                    item_text = small_font.render(f"{item}", True, WHITE) # Removed the x count
                    screen.blit(item_text, item_text.get_rect(center=(right_x + right_width // 2, y + button_h // 2)))
        elif self.state == "stances":
            for i, stance in enumerate(self.stance_options):
                y = start_y + i * (button_h + 8)
                if stance == self.player.current_stance:
                    color = (50, 200, 50) # Darker green for active
                elif i == self.selected_stance:
                    color = wood_light
                else:
                    color = wood_base
                pygame.draw.rect(screen, color, (right_x, y, right_width, button_h), border_radius=10)
                pygame.draw.rect(screen, wood_dark, (right_x, y, right_width, button_h), 2, border_radius=10)
                stance_text = small_font.render(stance, True, WHITE)
                screen.blit(stance_text, stance_text.get_rect(center=(right_x + right_width // 2, y + button_h // 2)))
        else:
            stats_y = panel_top + 10
            screen.blit(small_font.render(self.player.name, True, WHITE), (right_x, stats_y))
            hp_color = GREEN if self.player.hp > 30 else RED
            screen.blit(small_font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, hp_color), (right_x, stats_y + 25))

        msg = self.message if self.message else "What will you do?"
        msg_text = font.render(msg, True, WHITE)
        screen.blit(msg_text, msg_text.get_rect(center=circle_center))

    def enemy_turn(self):
        self.state = "enemy_turn"
        enemy_moves_dict = self.enemy.moves


        # --- DEBUG BLOCK ---
        move_names = list(enemy_moves_dict.keys())
        move_weights = list(enemy_moves_dict.values())
        
        # Calculate actual percentages for the console
        total_weight = sum(move_weights)
        debug_probs = {name: f"{(weight/total_weight)*100}%" for name, weight in enemy_moves_dict.items()}
        print(f"DEBUG: Move Pool Probabilities: {debug_probs}")
        # -------------------

        move_name = random.choices(move_names, weights=move_weights, k=1)[0]
        print(f"DEBUG: RNG Selected -> {move_name}")

        # 1. Pick the move
        # Since self.enemy is now an instance of your Enemy class
        move_data = ENEMY_MOVES.get(move_name)
        
        # 2. Display Message
        self.message = f"{self.enemy.name} used {move_name}! {move_data['text']}"
        
        # 3. Apply Effect (Universal AI switchboard)
        effect = move_data.get("effect")
        if effect == "poison":
            self.player.poisoned = True
            self.message += " You are poisoned!"

        elif effect == "buff_atk":
            self.enemy.attack_stat = int(self.enemy.attack_stat * 1.5)
            self.message = f"{self.enemy.name}'s power surged massively!"

        elif effect == "stat_swap":
            self.enemy.attack_stat, self.enemy.defense_stat = self.enemy.defense_stat, self.enemy.attack_stat

        elif effect == "recoil":
            self.enemy.hp -= 10
            
        # 4. Damage Calculation
        # Use the move's base damage + the Enemy's dynamic attack property
        base_power = move_data.get("damage", 0)

        if base_power > 0:
            total_power = base_power + self.enemy.attack # This uses your @property!
            
            # Your take_damage formula handles the defense and stances automatically
            actual_dmg = self.player.take_damage(total_power)
        self.message_timer = 90

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN: return
        
        if self.state == "menu":
            if event.key == pygame.K_UP: self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN: self.selected_option = (self.selected_option + 1) % 4
            elif event.key in (pygame.K_RETURN, pygame.K_z): self.execute_action(self.menu_options[self.selected_option])
        
        elif self.state == "stances":
            if event.key == pygame.K_UP: self.selected_stance = (self.selected_stance - 1) % len(self.stance_options)
            elif event.key == pygame.K_DOWN: self.selected_stance = (self.selected_stance + 1) % len(self.stance_options)
            elif event.key in (pygame.K_RETURN, pygame.K_z): 
                self.set_stance(self.stance_options[self.selected_stance])
            elif event.key in (pygame.K_ESCAPE, pygame.K_x): self.state = "menu"

        elif self.state == "items":
            if event.key == pygame.K_UP: self.selected_item = max(0, self.selected_item - 1)
            elif event.key == pygame.K_DOWN: self.selected_item = min(len(self.item_options) - 1, self.selected_item + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_z): self.use_item(self.item_options[self.selected_item])
            elif event.key in (pygame.K_ESCAPE, pygame.K_x): self.state = "menu"
=======
        gap = 8
        button_h = min(45, (available_h - gap * (n - 1)) // n)
        total_btn_h = button_h * n
        gap = (available_h - total_btn_h) // max(n - 1, 1)
        gap = max(4, min(gap, 16))

        total_height = total_btn_h + gap * (n - 1)
        start_y = panel_top + (panel_height - total_height) // 2

        for i, option in enumerate(self.menu_options):
            y = start_y + i * (button_h + gap)
            color = wood_light if (self.state == "menu" and i == self.selected_option) else wood_base
            pygame.draw.rect(logical, color, (left_x, y, left_width, button_h), border_radius=10)
            pygame.draw.rect(logical, wood_dark, (left_x, y, left_width, button_h), 2, border_radius=10)
            text = small_font.render(option, True, WHITE)
            logical.blit(text, text.get_rect(center=(left_x + left_width // 2, y + button_h // 2)))

        if self.state == "items":
            ni = len(self.item_options) if self.item_options else 1
            item_button_h = min(45, (available_h - gap * (ni - 1)) // ni)
            item_total_h = item_button_h * ni + gap * (ni - 1)
            item_start_y = panel_top + (panel_height - item_total_h) // 2

            if self.item_options:
                for i, item in enumerate(self.item_options):
                    y = item_start_y + i * (item_button_h + gap)
                    color = wood_light if i == self.selected_item else wood_base
                    pygame.draw.rect(logical, color, (right_x, y, right_width, item_button_h), border_radius=10)
                    pygame.draw.rect(logical, wood_dark, (right_x, y, right_width, item_button_h), 2, border_radius=10)
                    text = small_font.render(f"{item} x{self.player.items[item]}", True, WHITE)
                    logical.blit(text, text.get_rect(center=(right_x + right_width // 2, y + item_button_h // 2)))

        if self.state != "items":
            stats_y = panel_top + 10
            name_text = small_font.render(self.player.name, True, WHITE)
            logical.blit(name_text, (right_x, stats_y))
            hp_text = small_font.render(
                f"HP: {self.player.hp}/{self.player.max_hp}",
                True,
                GREEN if self.player.hp > 30 else RED
            )
            logical.blit(hp_text, (right_x, stats_y + 25))

        msg = self.message if self.message else "What will you do?"
        msg_text = font.render(msg, True, WHITE)
        logical.blit(msg_text, msg_text.get_rect(center=circle_center))

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if self.state == "menu":
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 4
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 4
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
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

    def execute_action(self, action):
        self.player.defending = False
        if action == "Attack":
            attack_result = roll_attack()
            roll = attack_result['roll']
            if attack_result['result_type'] == 'critical_fail':
                self_damage = sum(roll_dice(2, 6))
                self.player.hp = max(0, self.player.hp - self_damage)
<<<<<<< HEAD
                self.message = f"Roll: {roll} - Critical Fail! Ouch: {self_damage}!"
=======
                self.message = f"Roll: {roll} - Critical Fail! Hurt yourself for {self_damage}!"
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
            elif attack_result['result_type'] == 'miss':
                self.message = f"Roll: {roll} - Miss!"
            else:
                damage = calculate_damage(attack_result, self.player.attack)
                actual_damage = self.enemy.take_damage(damage)
                self.message = f"Roll: {roll} - {attack_result['message']} {actual_damage} damage!"
                self.shake_timer = 10
            self.message_timer = 90
            self.state = "animating"
<<<<<<< HEAD
        elif action == "Stances":
            self.state = "stances"
            self.selected_stance = 0
        elif action == "Items":
            # Instead of looking at a dictionary, look at the inventory list
            # Filter out 'air' so the player only sees real items
            self.item_options = [item[0] for item in self.player_inventory.inventory if item != 'air']
            if self.item_options: 
=======
        elif action == "Items":
            self.item_options = [k for k, v in self.player.items.items() if v > 0]
            if self.item_options:
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
                self.state = "items"
                self.selected_item = 0
        elif action == "Defend":
            self.player.defending = True
            self.message = "Bracing for impact!"
            self.message_timer = 60
            self.state = "animating"
        elif action == "Run Away":
            self.message = "Escaped!"
            self.state = "victory"; self.message_timer = 60

    def set_stance(self, stance_name):
        if self.player.current_stance == stance_name:
            self.message = f"Already in {stance_name}!"
            return

        self.player.current_stance = stance_name
        self.message = f"Shifted to {stance_name} Stance!"
        self.message_timer = 60
<<<<<<< HEAD
        self.state = "animating" # This triggers the update() to go to enemy_turn
    
    def use_item(self, item_name):
        for i, item in enumerate(self.player_inventory.inventory):
            if item != 'air' and item[0] == item_name:
                heal = item[3] 
                self.player.hp = min(self.player.max_hp, self.player.hp + heal)
                self.player_inventory.inventory[i] = 'air' 
                
                self.message = f"Used {item_name}! Healed {heal}!"
                self.message_timer = 90  # Give the player time to read it
                self.state = "animating" # This tells update() to trigger the enemy turn
                break
=======
        self.state = "animating"
        self.item_options = [k for k, v in self.player.items.items() if v > 0]
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

    def update(self):
        if not self.player.is_alive() and self.state != "defeat":
            self.message = "You died..."
            self.state = "defeat"
            self.message_timer = 90
            return # Stop other logic so the death message stays up
        
        if self.message_timer > 0:
            self.message_timer -= 1
<<<<<<< HEAD
            
        # ONLY proceed to the next turn state if the current message is done showing
        if self.message_timer == 0:
            if self.state in ("victory", "defeat"): 
                self.battle_over = True
                return
                
            if self.state == "animating":
=======
            if self.message_timer == 0 and self.state not in ("victory", "defeat"):
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
                if not self.enemy.is_alive():
                    self.player.gain_xp(self.enemy.xp_reward)
                    self.message = f"{self.enemy.name} defeated!"
                    self.state = "victory"
<<<<<<< HEAD
                    self.message_timer = 90
                else: 
                    self.enemy_turn()

            # FIXED: Only start the player turn AFTER the enemy's move message timer hits 0
            elif self.state == "enemy_turn":
                if not self.player.is_alive():
                    self.message = "You died..."
                    self.state = "defeat"
                    self.message_timer = 90
                else: 
                    self.start_player_turn()
    
    def start_player_turn(self):
        self.state = "menu"
        
        # Check for poison
        # Note: Ensure 'poisoned' is defined in your Player class
        if hasattr(self.player, "poisoned") and self.player.poisoned:
            poison_dmg = 5 
            self.player.hp = max(0, self.player.hp - poison_dmg)
            self.message = f"Poison dealt {poison_dmg} damage!"
            self.message_timer = 60 # Brief pause so player sees the damage

    def run(self):
        self.battle_over = False
        while not self.battle_over:
=======
                    self.message_timer = 120
                    return
                if not self.player.is_alive():
                    self.message = "You were defeated..."
                    self.state = "defeat"
                    self.message_timer = 120
                    return
                self.message = ""
                self.state = "menu"
        if self.state in ("victory", "defeat") and self.message_timer == 0:
            self.battle_over = True

    def draw(self):
        self.draw_battle_scene()
        self.draw_menu()
        blit_letterboxed(logical, screen)

    def run(self):
        self.battle_over = False
        while True:
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                self.handle_input(event)
            self.update()
            screen.fill(BLACK) # Clear before drawing
            self.draw_battle_scene()
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)
<<<<<<< HEAD
        return "WIN" if self.state == "victory" else "LOSE"

def run_battle(game_screen, player, inventory_sys, enemy_name):
    global screen
=======

            if self.battle_over:
                return "WIN" if self.state == "victory" else "LOSE"

        return "QUIT"


def run_battle(game_screen):
    global screen, logical
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
    screen = game_screen
    logical = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    init_fonts()
<<<<<<< HEAD
    battle = BattleSystem(player, inventory_sys,enemy_name)
    result = battle.run()
    return result, player
=======
    pygame.display.set_caption("yes we're fighting ryan gosling")
    battle = BattleSystem()
    return battle.run()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    logical = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("yes we're fighting ryan gosling")
    init_fonts()
    battle = BattleSystem()
    result = battle.run()
    print(f"Battle result: {result}")
    pygame.quit()
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
