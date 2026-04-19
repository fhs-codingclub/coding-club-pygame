import json
import os
import pygame

# Fallback font for missing images
pygame.font.init()
debug_font = pygame.font.SysFont("Arial", 20)

class Combatant:
    def __init__(self, name, max_hp, attack, defense, current_hp=None):
        self.name = name
        self.max_hp = max_hp
        self.hp = current_hp if current_hp is not None else max_hp
        self.attack_stat = attack  # Base stat
        self.defense_stat = defense # Base stat
        
        # Stance modifiers: (Attack Multiplier, Defense Multiplier)
        self.STANCES = {
            "Neutral": (1.0, 1.0),
            "Aggressive": (1.5, 0.5), # Glass Cannon: High ATK, Low DEF
            "Iron": (0.6, 2.0),       # Tank: Low ATK, High DEF
            "Berserk": (2.0, 0.2)      # High Risk: Massive ATK, effectively no DEF
        }
        self.current_stance = "Neutral"
        self.defending = False

    @property
    def attack(self):
        # f(a) = base_attack * stance_multiplier
        atk_mult = self.STANCES[self.current_stance][0]
        return int(self.attack_stat * atk_mult)

    def take_damage(self, incoming_damage):
        # 1. Calculate effective defense based on stance and guarding
        stance_def_mult = self.STANCES[self.current_stance][1]
        guard_mult = 2.0 if self.defending else 1.0
        
        effective_defense = self.defense_stat * stance_def_mult * guard_mult
        
        # 2. Logarithmic Reduction Formula: f(d) = 100 / (100 + d)
        reduction_factor = 100 / (100 + effective_defense)
        
        actual_damage = max(1, int(incoming_damage * reduction_factor))
        self.hp = max(0, self.hp - actual_damage)
        
        return actual_damage

    def is_alive(self):
        return self.hp > 0

class Enemy(Combatant):
    def __init__(self, enemy_name):
        # script_dir is 'py' folder
        script_dir = os.path.dirname(__file__)
        
        # 1. Load Enemy Data
        json_path = os.path.join(script_dir, "assets", "jason", "enemies.json")
        all_enemies = {}
        
        try:
            with open(json_path, "r") as f:
                all_enemies = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: Could not load {json_path}")

        # 2. Extract specific enemy data
        # Search case-insensitively just in case
        data = next((v for k, v in all_enemies.items() if k.lower() == enemy_name.lower()), None)
        
        if not data:
            data = {"hp": 50, "attack": 10, "defense": 5, "xp_reward": 20, "image": "placeholder.png"}
        else:
            # If found, ensure we use the properly capitalized name from the JSON
            enemy_name = next(k for k in all_enemies.keys() if k.lower() == enemy_name.lower())

        # 3. Initialize Combatant Stats
        super().__init__(
            name=enemy_name, 
            max_hp=data["hp"], 
            attack=data["attack"], 
            defense=data["defense"]
        )
        self.xp_reward = data.get("xp_reward", 0)

        # 4. Handle Image Loading
        # Images are in 'assets/img/' inside the 'py' folder
        img_file = data.get("image", "placeholder.png")
        img_path = os.path.join(script_dir, "assets", "img", img_file)
        
        self.image = self._load_scaled_image(img_path)

    def _load_scaled_image(self, path):
        """Loads image or returns a red placeholder square if missing."""
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.scale(img, (150, 150))
            except pygame.error:
                pass
        
        # Placeholder logic
        surf = pygame.Surface((150, 150))
        surf.fill((255, 50, 50))
        text = debug_font.render(self.name, True, (255, 255, 255))
        surf.blit(text, (10, 65))
        return surf