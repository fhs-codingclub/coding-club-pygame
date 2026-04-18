import pygame
import json
import os  # Need this for the path joining

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size=48):
        super().__init__()
        self.name = "Hero" # Use a string here instead of the 'name' import
        
        # 1. Overworld Data
        self.grid_x = x
        self.grid_y = y
        self.tile_size = tile_size
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 255, 0)) 
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))

        # 2. Stats
        self.level = 1
        self.xp = 0
        self.max_hp = 100
        self.hp = 100
        self.attack = 15
        self.defense = 5
        self.items = {"Hamburger": 3, "Lifeup": 1}

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def is_alive(self):
        return self.hp > 0
    
    def gain_xp(self, amount):
        self.xp += amount
        self.check_levelup()

    def use_item(self, item_name):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            heal_amount = 20
            self.hp = min(self.max_hp, self.hp + heal_amount)
            return heal_amount
        return 0
    
    def check_levelup(self):
        try:
            # Code inside the function MUST be indented
            path = os.path.join("py", "assets", "jason", "levelUpXp.json")
            if not os.path.exists(path):
                print(f"File not found: {path}")
                return

            with open(path, 'r') as f:
                xp_requirements = json.load(f)
                
            current_level_str = str(self.level)
            
            if current_level_str in xp_requirements:
                req = xp_requirements[current_level_str]
                if self.xp >= req:
                    self.level += 1
                    self.attack += 5
                    self.max_hp += 20
                    self.hp = self.max_hp
                    print(f"LEVEL UP! Now Level {self.level}")
                    
                    # Check again in case they have enough for another level
                    self.check_levelup() 
                    
        except Exception as e:
            print(f"XP JSON Error: {e}")

    def update_position(self):
        self.rect.topleft = (self.grid_x * self.tile_size, self.grid_y * self.tile_size)