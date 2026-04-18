import pygame

class NPC(pygame.sprite.Sprite):
    def __init__(self, name, x, y, dialogue_list, tile_size=48):
        super().__init__()
        # 1. Load and Crop
        try:
            self.image = pygame.image.load("py/assets/img/vivi-right.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        except Exception as e:
            print(f"Error loading NPC image: {e}")
            self.image = pygame.Surface((tile_size, tile_size))
            self.image.fill((255, 0, 255))

        # 3. SET THE GRID COORDINATES (This fixes your error!)
        self.grid_x = x
        self.grid_y = y
        
        # 4. Set the rect for drawing (converting grid to pixels)
        self.rect = self.image.get_rect(topleft=(x * tile_size, y * tile_size))
        
        self.name = name
        self.dialogue = dialogue_list
        self.dialogue_index = 0
        self.is_talking = False

    def get_current_line(self):
        return self.dialogue[self.dialogue_index]

    def advance_dialogue(self):
        if self.dialogue_index < len(self.dialogue) - 1:
            self.dialogue_index += 1
            return True # Still talking
        else:
            self.is_talking = False
            self.dialogue_index = 0
            return False # Finished talking