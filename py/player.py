import pygame
import json
import os  # Need this for the path joining

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size=48):
        super().__init__()
        self.name = "Kim" 
        
        # 1. Overworld Data
        self.grid_x = x
        self.grid_y = y
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 255, 0)) 
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))

        # 2. Stats
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        self.max_hp = 100
        self.hp = 100
        self.base_attack = 15
        self.defense = 5

        self.current_stance = "Neutral"
        self.defending = False
        self.stances = {
            "Neutral":    {"def": 1.0, "atk": 1.0},
            "Aggressive": {"def": 1.3, "atk": 1.5},
            "Iron":       {"def": 0.5, "atk": 0.7},
            "Berserk":    {"def": 1.8, "atk": 2.0}
        }

    @property
    def attack(self):
        stance_data = self.stances.get(self.current_stance, {"atk": 1.0})
        atk_mult = stance_data.get("atk", 1.0)
        
        return int(self.base_attack * atk_mult)
    
    # In player.py inside the Player class

    def take_damage(self, amount):
        # Look up the multiplier based on the current stance
        # .get() is safer than [], it defaults to 1.0 if the stance isn't found
        multiplier = self.stances.get(self.current_stance, {}).get("def", 1.0)
        
        final_damage = int(amount * multiplier)
        self.hp = max(0, self.hp - final_damage)
        return final_damage

    def is_alive(self):
        return self.hp > 0
    
    def gain_xp(self, amount):
        self.xp += amount
        self.check_levelup()
    
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
                self.xp_to_next_level = req
                # In Player.py inside check_levelup:
            if self.xp >= req:
                self.level += 1
                self.base_attack += 5  # Change this from self.attack
                self.defense += 2      # Let's give some defense on level up too
                self.max_hp += 20
                self.hp = self.max_hp
                    
        except Exception as e:
            print(f"XP JSON Error: {e}")

    def update_position(self):
        self.rect.topleft = (self.grid_x * self.tile_size, self.grid_y * self.tile_size)