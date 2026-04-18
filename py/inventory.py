import pygame
import json

# --- Colors ---
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

# Load the JSON data
try:
    with open('py/assets/jason/items.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: items.json not found!")
    data = {}

class InventorySystem:
    def __init__(self, screen_width=400, screen_height=300):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.UI_SCALE = screen_width / 400
        
        # --- Inventory slots ---
        self.inventory = ['air'] * 8
        self.armor = 'air'
        self.weapon = 'air'
        
        # --- Selection state ---
        self.inventory_selected = 10  
        self.inventory_hover = 10
        self.is_open = False
        
        self._setup_inventory_rects()
        
        # --- Fonts ---
        self.font2 = pygame.font.Font(None, int(15 * self.UI_SCALE))
        self.font3 = pygame.font.Font(None, int(10 * self.UI_SCALE))
        self.font4 = pygame.font.Font(None, int(12 * self.UI_SCALE))
    
    def _setup_inventory_rects(self):
        UI = self.UI_SCALE
        self.inventory_list = [
            pygame.Rect(115*UI, 95*UI, 35*UI, 45*UI),
            pygame.Rect(160*UI, 95*UI, 35*UI, 45*UI),
            pygame.Rect(205*UI, 95*UI, 35*UI, 45*UI),
            pygame.Rect(250*UI, 95*UI, 35*UI, 45*UI),
            pygame.Rect(115*UI, 160*UI, 35*UI, 45*UI),
            pygame.Rect(160*UI, 160*UI, 35*UI, 45*UI),
            pygame.Rect(205*UI, 160*UI, 35*UI, 45*UI),
            pygame.Rect(250*UI, 160*UI, 35*UI, 45*UI),
        ]
        self.armor_space = pygame.Rect(60*UI, 95*UI, 35*UI, 45*UI)
        self.weapon_space = pygame.Rect(60*UI, 160*UI, 35*UI, 45*UI)
        self.use_button_rect = pygame.Rect(245*UI, 255*UI, 35*UI, 20*UI)
    
    def add_item_by_name(self, item_name):
        if item_name in data:
            item_info = data[item_name]
            new_item = [
                item_name, 
                item_info.get("description", "No description"),
                item_info.get("type", "misc"),
                item_info.get("value", 0),
                None 
            ]
            return self.add_item(new_item)
        return False

    def add_item(self, item):
        for i in range(8):
            if self.inventory[i] == "air":
                self.inventory[i] = item
                return True
        return False
    
    def toggle(self):
        self.is_open = not self.is_open
        if not self.is_open:
            self.inventory_selected = 10
    
    def handle_event(self, event, player): # Added player here
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.toggle()
            return True
        
        if not self.is_open:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.inventory_hover != 10:
            self._handle_click(player) # Added player here
            return True
        
        return False
    
    def _handle_click(self, player):
        if self.inventory_hover == 20:  
            self._use_selected_item(player) # Added player here
        elif self.inventory_hover == 21:  
            self._unequip_armor(player)
        elif self.inventory_hover == 22:  
            self._unequip_weapon(player)
        else:  
            self._handle_slot_click(self.inventory_hover)
    
    def _handle_slot_click(self, index):
        # If we click the same slot twice, deselect it
        if self.inventory_selected == index:
            self.inventory_selected = 10
        else:
            self.inventory_selected = index

    def _use_selected_item(self, player): # Added player here
        if self.inventory_selected == 10 or self.inventory[self.inventory_selected] == "air":
            return
        
        item = self.inventory[self.inventory_selected]
        item_type = item[2].lower() # Force lowercase to match JSON
        item_value = item[3]
        
        if item_type == "weapon":
            old_weapon = self.weapon
            self.weapon = item
            player.attack += item_value # Update actual player stats
            self.inventory[self.inventory_selected] = old_weapon
        elif item_type == "armor":
            old_armor = self.armor
            self.armor = item
            player.defense += item_value
            self.inventory[self.inventory_selected] = old_armor
        elif item_type == "healing":
            player.hp = min(player.hp + item_value, player.max_hp)
            print(f"Used {item[0]}! HP is now {player.hp}")
            self.inventory[self.inventory_selected] = "air"
        
        self.inventory_selected = 10
    
    # ... (Keep your unequip functions, just ensure they adjust player.attack/defense) ...

    def update(self):
        if not self.is_open:
            return
        mouse_pos = pygame.mouse.get_pos()
        self.inventory_hover = 10
        for i, rect in enumerate(self.inventory_list):
            if rect.collidepoint(mouse_pos):
                self.inventory_hover = i
                return
        if self.use_button_rect.collidepoint(mouse_pos):
            self.inventory_hover = 20
        elif self.armor_space.collidepoint(mouse_pos):
            self.inventory_hover = 21
        elif self.weapon_space.collidepoint(mouse_pos):
            self.inventory_hover = 22
    
    def draw(self, screen, player):
        if not self.is_open:
            return
        UI = self.UI_SCALE
        # Draw panels
        pygame.draw.rect(screen, GRAY, (310*UI, 50*UI, 90*UI, 200*UI))
        pygame.draw.rect(screen, GRAY, (50*UI, 75*UI, 250*UI, 150*UI))
        pygame.draw.rect(screen, GRAY, (100*UI, 250*UI, 200*UI, 50*UI))

        # Stats Text
        screen.blit(self.font4.render(f"Attack: {player.attack}", True, (0, 0, 0)), (320*UI, 60*UI))
        screen.blit(self.font4.render(f"Health: {int(player.hp)}/{player.max_hp}", True, (0, 0, 0)), (320*UI, 110*UI))
        screen.blit(self.font4.render(f"XP: {player.xp}/{player.xp_to_next_level}", True, (0, 0, 0)), (320*UI, 160*UI))
        screen.blit(self.font4.render(f"Level: {player.level}", True, (0, 0, 0)), (320*UI, 210*UI))

        # Inventory Slots
        for i, rect in enumerate(self.inventory_list):
            color = (200, 200, 200) if i == self.inventory_selected else WHITE
            pygame.draw.rect(screen, color, rect)
            if self.inventory[i] != "air":
                pygame.draw.rect(screen, (0, 150, 255), rect.inflate(-6, -6))
                name_surf = self.font3.render(self.inventory[i][0], True, (0, 0, 0))
                screen.blit(name_surf, name_surf.get_rect(center=rect.center))

        # Equipment Slots
        pygame.draw.rect(screen, WHITE, self.armor_space)
        pygame.draw.rect(screen, WHITE, self.weapon_space)

        # Use Button & Description
        if self.inventory_selected != 10 and self.inventory[self.inventory_selected] != "air":
            item = self.inventory[self.inventory_selected]
            screen.blit(self.font2.render(item[0], True, (0, 0, 0)), (110*UI, 260*UI))
            screen.blit(self.font3.render(item[1], True, (0, 0, 0)), (110*UI, 275*UI))
            pygame.draw.rect(screen, (200, 200, 200), self.use_button_rect)
            screen.blit(self.font2.render("Use", True, (0, 0, 0)), (247*UI, 258*UI))