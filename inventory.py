import pygame
import random
import os
import json

# --- Colors ---
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

with open('jason/test.json', 'r') as file:
    data = json.load(file)

class InventorySystem:
    
    def __init__(self, screen_width=400, screen_height=300):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.UI_SCALE = screen_width / 400
        
        # --- Stats ---
        self.attack = 15
        self.defense = 5
        self.health = 100
        self.maxhealth = 100
        
        # --- Inventory slots ---
        self.inventory = ['air'] * 8
        self.armor = 'air'
        self.weapon = 'air'
        
        # --- Selection state ---
        self.inventory_selected = 10  # 10 means no item selected
        self.inventory_hover = 10
        self.is_open = False
        
        # --- Setup inventory slot rectangles ---
        self._setup_inventory_rects()
        
        # --- Fonts ---
        self.font2 = pygame.font.Font(None, 15 * round(self.UI_SCALE))
        self.font3 = pygame.font.Font(None, 8 * round(self.UI_SCALE))
        self.font4 = pygame.font.Font(None, 12 * round(self.UI_SCALE))
    
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
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            self.toggle()
            return True
        
        if not self.is_open:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.inventory_hover != 10:
            self._handle_click()
            return True
        
        return False
    
    def _handle_click(self):
        if self.inventory_hover == 20:  # Use button
            self._use_selected_item()
        elif self.inventory_hover == 21:  # Armor slot
            self._unequip_armor()
        elif self.inventory_hover == 22:  # Weapon slot
            self._unequip_weapon()
        else:  # Regular inventory slot
            self._handle_slot_click(self.inventory_hover)
    
    def _use_selected_item(self):
        if self.inventory_selected == 10 or self.inventory[self.inventory_selected] == "air":
            return
        
        item = self.inventory[self.inventory_selected]
        item_type = item[2]
        
        if item_type == "weapon":
            old_weapon = self.weapon
            self.weapon = item
            self.inventory[self.inventory_selected] = old_weapon
            self.attack = item[3]
        elif item_type == "armor":
            old_armor = self.armor
            self.armor = item
            self.inventory[self.inventory_selected] = old_armor
            self.defense = item[3]
        else:  # Healing/consumable
            self.health = min(self.health + item[3], self.maxhealth)
            self.inventory[self.inventory_selected] = "air"
        
        self.inventory_selected = 10
    
    def _unequip_armor(self):
        if self.armor == "air":
            return
        if self.add_item(self.armor):
            self.armor = "air"
            self.defense = 5
    
    def _unequip_weapon(self):
        if self.weapon == "air":
            return
        if self.add_item(self.weapon):
            self.weapon = "air"
            self.attack = 15
    
    def _handle_slot_click(self, slot_index):
        if self.inventory_selected == slot_index:
            self.inventory_selected = 10
        elif self.inventory_selected == 10:
            self.inventory_selected = slot_index
        else:
            # Swap items
            self.inventory[self.inventory_selected], self.inventory[slot_index] = \
                self.inventory[slot_index], self.inventory[self.inventory_selected]
            self.inventory_selected = 10
    
    def update(self):
        if not self.is_open:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        self.inventory_hover = 10
        
        # Check inventory slots
        for i, rect in enumerate(self.inventory_list):
            if rect.collidepoint(mouse_pos):
                self.inventory_hover = i
                return
        
        # Check use button
        if self.use_button_rect.collidepoint(mouse_pos):
            self.inventory_hover = 20
        elif self.armor_space.collidepoint(mouse_pos):
            self.inventory_hover = 21
        elif self.weapon_space.collidepoint(mouse_pos):
            self.inventory_hover = 22
    
    def draw(self, screen):
        if not self.is_open:
            return
        
        UI = self.UI_SCALE
        
        # Draw stats panel
        pygame.draw.rect(screen, GRAY, (310*UI, 50*UI, 90*UI, 200*UI))
        stats_text1 = self.font4.render(f"Attack: {self.attack}", True, (0, 0, 0))
        stats_text2 = self.font4.render(f"Defense: {self.defense}", True, (0, 0, 0))
        stats_text3 = self.font4.render(f"Health: {self.health}/{self.maxhealth}", True, (0, 0, 0))
        screen.blit(stats_text1, (320*UI, 60*UI))
        screen.blit(stats_text2, (320*UI, 85*UI))
        screen.blit(stats_text3, (320*UI, 110*UI))
        
        # Draw main inventory panel
        pygame.draw.rect(screen, GRAY, (50*UI, 75*UI, 250*UI, 150*UI))
        pygame.draw.rect(screen, GRAY, (100*UI, 250*UI, 200*UI, 50*UI))
        
        # Draw inventory slots
        for i, rect in enumerate(self.inventory_list):
            color = (200, 200, 200) if i == self.inventory_selected else WHITE
            pygame.draw.rect(screen, color, rect)
            if self.inventory[i] != "air":
                img = pygame.transform.scale(pygame.image.load(self.inventory[i][4]), (int(35*UI), int(45*UI)))
                screen.blit(img, rect.topleft)
        
        # Draw armor slot
        pygame.draw.rect(screen, WHITE, self.armor_space)
        if self.armor != "air":
            img = pygame.transform.scale(pygame.image.load(self.armor[4]), (int(35*UI), int(45*UI)))
            screen.blit(img, self.armor_space.topleft)
        
        # Draw weapon slot
        pygame.draw.rect(screen, WHITE, self.weapon_space)
        if self.weapon != "air":
            img = pygame.transform.scale(pygame.image.load(self.weapon[4]), (int(35*UI), int(45*UI)))
            screen.blit(img, self.weapon_space.topleft)
        
        # Draw item description if something is selected
        if self.inventory_selected != 10:
            item = self.inventory[self.inventory_selected]
            if item == "air":
                desc_text = self.font3.render("Literally nothing", True, (0, 0, 0))
                screen.blit(desc_text, (110*UI, 260*UI))
            else:
                title_text = self.font2.render(item[0], True, (0, 0, 0))
                desc_text = self.font3.render(item[1], True, (0, 0, 0))
                screen.blit(title_text, (110*UI, 260*UI))
                screen.blit(desc_text, (110*UI, 275*UI))
                pygame.draw.rect(screen, (200, 200, 200), self.use_button_rect)
                use_text = self.font2.render("Use", True, (0, 0, 0))
                screen.blit(use_text, (250*UI, 260*UI))


# --- Legacy standalone mode (for testing) ---
if __name__ == "__main__":
    pygame.init()
    
    WIDTH = 600
    HEIGHT = int(WIDTH * (3/4))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Inventory Test")
    
    clock = pygame.time.Clock()
    inventory_system = InventorySystem(WIDTH, HEIGHT)
    
    # Add some test items
    item1 = data.item1
    item2 = data.item2
    item3 = data.item3
    inventory_system.add_item(item1)
    inventory_system.add_item(item2)
    inventory_system.add_item(item3)
    
    running = True
    while running:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            inventory_system.handle_event(event)
        
        inventory_system.update()
        
        screen.fill((255, 255, 255))
        inventory_system.draw(screen)
        
        if not inventory_system.is_open:
            font = pygame.font.Font(None, 30)
            text = font.render("Press E to open inventory", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - 100, HEIGHT//2))
        
        pygame.display.update()
    
    pygame.quit()
