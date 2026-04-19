import pygame
import random
import os
import sys

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))

from py import inventory
from Enemy import Enemy 
from moves import MOVES  
from dice import roll_attack, calculate_damage, roll_dice

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = None

# Colors
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

class BattleSystem:
    def __init__(self, player, enemy_name="Ryan Gosling"):
        self.player = player
        self.enemy = Enemy(enemy_name)

        self.state = "menu"
        self.menu_options = ["Attack", "Items", "Defend", "Run Away"]
        self.selected_option = 0

        self.item_options = list(self.player.items.keys())
        self.selected_item = 0

        self.message = ""
        self.message_timer = 0
        self.clock = pygame.time.Clock()
        self.shake_timer = 0
        self.enemy_offset = [0, 0]

    def draw_hp_bar(self, x, y, current_hp, max_hp, width=200):
        ratio = max(0, min(current_hp / max_hp, 1))
        pygame.draw.rect(screen, BLACK, (x, y, width, 20))
        color = GREEN if ratio > 0.5 else YELLOW if ratio > 0.25 else RED
        pygame.draw.rect(screen, color, (x, y, int(width * ratio), 20))
        pygame.draw.rect(screen, WHITE, (x, y, width, 20), 2)
        hp_text = small_font.render(f"{current_hp}/{max_hp}", True, WHITE)
        screen.blit(hp_text, (x + width + 10, y))

    def draw_battle_scene(self):
        screen.fill(DARK_BLUE)
        time = pygame.time.get_ticks() / 1000
        for i in range(0, SCREEN_WIDTH, 40):
            for j in range(0, 240, 40):
                color_val = int((i + j + time * 50) % 100) + 20
                pygame.draw.circle(screen, (color_val // 2, color_val // 2, color_val), (i + 20, j + 20), 15)

        enemy_x = SCREEN_WIDTH // 2 - 75 + self.enemy_offset[0]
        enemy_y = 50 + self.enemy_offset[1]
        
        # Draw Enemy Image (or placeholder if image missing)
        screen.blit(self.enemy.image, (enemy_x, enemy_y))

        self.draw_hp_bar(SCREEN_WIDTH // 2 - 100, 210, self.enemy.hp, self.enemy.max_hp)
        enemy_name_text = small_font.render(self.enemy.name, True, WHITE)
        screen.blit(enemy_name_text, (SCREEN_WIDTH // 2 - 30, 190))

    def draw_menu(self):
        wood_base = (120, 80, 40)
        wood_dark = (80, 50, 20)
        wood_light = (160, 120, 60)
        wood_circle = (140, 100, 60)
        wood_grid = (100, 70, 40)

        panel_height = 180
        panel_top = SCREEN_HEIGHT - panel_height

        pygame.draw.rect(screen, wood_base, (0, panel_top, SCREEN_WIDTH, panel_height))
        pygame.draw.rect(screen, wood_dark, (0, panel_top, SCREEN_WIDTH, panel_height), 8)

        circle_radius = 110
        circle_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - panel_height // 2)

        pygame.draw.circle(screen, wood_circle, circle_center, circle_radius)
        pygame.draw.circle(screen, wood_dark, circle_center, circle_radius, 8)

        for r in range(10, circle_radius, 15):
            pygame.draw.circle(screen, wood_grid, circle_center, r, 2)

        padding = 10
        left_x = padding
        left_width = max((circle_center[0] - circle_radius) - padding * 2, 10)
        right_x = circle_center[0] + circle_radius + padding
        right_width = max(SCREEN_WIDTH - right_x - padding, 10)

        n = len(self.menu_options)
        available_h = panel_height - 20
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
                    item_text = small_font.render(f"{item} x{self.player.items[item]}", True, WHITE)
                    screen.blit(item_text, item_text.get_rect(center=(right_x + right_width // 2, y + button_h // 2)))
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
        damage = self.enemy.attack + random.randint(-2, 2)
        actual_damage = self.player.take_damage(damage)
        self.message = f"{self.enemy.name} attacks for {actual_damage} damage!"
        self.message_timer = 90

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN: return
        if self.state == "menu":
            if event.key == pygame.K_UP: self.selected_option = (self.selected_option - 1) % 4
            elif event.key == pygame.K_DOWN: self.selected_option = (self.selected_option + 1) % 4
            elif event.key in (pygame.K_RETURN, pygame.K_z): self.execute_action(self.menu_options[self.selected_option])
        elif self.state == "items":
            if event.key == pygame.K_UP: self.selected_item = max(0, self.selected_item - 1)
            elif event.key == pygame.K_DOWN: self.selected_item = min(len(self.item_options) - 1, self.selected_item + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_z): self.use_item(self.item_options[self.selected_item])
            elif event.key in (pygame.K_ESCAPE, pygame.K_x): self.state = "menu"

    def execute_action(self, action):
        self.player.defending = False
        if action == "Attack":
            attack_result = roll_attack()
            roll = attack_result['roll']
            if attack_result['result_type'] == 'critical_fail':
                self_damage = sum(roll_dice(2, 6))
                self.player.hp = max(0, self.player.hp - self_damage)
                self.message = f"Roll: {roll} - Critical Fail! Ouch: {self_damage}!"
            elif attack_result['result_type'] == 'miss':
                self.message = f"Roll: {roll} - Miss!"
            else:
                damage = calculate_damage(attack_result, self.player.attack)
                actual_damage = self.enemy.take_damage(damage)
                self.message = f"Roll: {roll} - {attack_result['message']} {actual_damage} damage!"
                self.shake_timer = 10
            self.message_timer = 90
            self.state = "animating"
        elif action == "Items":
            self.item_options = [k for k, v in self.player.items.items() if v > 0]
            if self.item_options: self.state = "items"; self.selected_item = 0
        elif action == "Defend":
            self.player.defending = True
            self.message = "Bracing for impact!"
            self.message_timer = 60
            self.state = "animating"
        elif action == "Run Away":
            self.message = "Escaped!"
            self.state = "victory"; self.message_timer = 60

    def use_item(self, item_name):
        heal = self.player.use_item(item_name)
        self.message = f"Used {item_name}! Healed {heal}!"
        self.message_timer = 60
        self.state = "animating"

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                if self.state in ("victory", "defeat"): self.battle_over = True; return
                if self.state == "animating":
                    if not self.enemy.is_alive():
                        self.player.gain_xp(self.enemy.xp_reward)
                        self.message = f"{self.enemy.name} defeated!"; self.state = "victory"; self.message_timer = 90
                    else: self.enemy_turn()
                elif self.state == "enemy_turn":
                    if not self.player.is_alive():
                        self.message = "You died..."; self.state = "defeat"; self.message_timer = 90
                    else: self.message = ""; self.state = "menu"

    def run(self):
        self.battle_over = False
        while not self.battle_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                self.handle_input(event)
            self.update()
            screen.fill(BLACK) # Clear before drawing
            self.draw_battle_scene()
            self.draw_menu()
            pygame.display.flip()
            self.clock.tick(60)
        return "WIN" if self.state == "victory" else "LOSE"

def run_battle(game_screen, player, enemy_name="Ryan Gosling"):
    global screen
    screen = game_screen
    init_fonts()
    battle = BattleSystem(player, enemy_name)
    result = battle.run()
    return result, player