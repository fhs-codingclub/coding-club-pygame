import pygame
import random
import sys
import os

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))
from inventory import InventorySystem

WIDTH = 400
HEIGHT = 300

def run_overworld(screen, inventory=None):
    """Run the overworld screen.
    
    Args:
        screen: The pygame display surface
        inventory: Optional InventorySystem instance. If None, creates a new one.
    
    Returns:
        Tuple of (action_string, inventory) - action is "QUIT", "START_BATTLE", or "RANDOM_BATTLE"
    """
    # --- Create or use existing inventory ---
    if inventory is None:
        inventory = InventorySystem(WIDTH, HEIGHT)
    
    # --- Local Settings ---
    TILE_SIZE = 20
    player_x_grid, player_y_grid = 0, 0
    target_x_grid, target_y_grid = 5, 5
    player_x = player_x_grid * TILE_SIZE
    player_y = player_y_grid * TILE_SIZE
    moving = False
    direction = None
    PLAYER_SPEED = 2
    
    # Random encounter settings
    ENCOUNTER_CHANCE = 0.10  # 10% chance per step (adjust as needed)
    
    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)
        screen.fill((34, 139, 34))  # Grass green BG
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("QUIT", inventory)
            
            # Let inventory handle its events first
            if inventory.handle_event(event):
                continue  # Event was consumed by inventory
            
            # Grid Movement Input (only when inventory is closed)
            if event.type == pygame.KEYDOWN and not moving and not inventory.is_open:
                if event.key == pygame.K_LEFT and player_x_grid > 0:
                    moving, direction = True, "left"
                elif event.key == pygame.K_RIGHT and player_x_grid < (WIDTH//TILE_SIZE)-1:
                    moving, direction = True, "right"
                elif event.key == pygame.K_UP and player_y_grid > 0:
                    moving, direction = True, "up"
                elif event.key == pygame.K_DOWN and player_y_grid < (HEIGHT//TILE_SIZE)-1:
                    moving, direction = True, "down"
                
                # TEST: Press SPACE to force a battle
                elif event.key == pygame.K_SPACE:
                    return ("RANDOM_BATTLE", inventory)
        
        # Update inventory (for mouse hover detection)
        inventory.update()
        
        # Interpolation (Smooth sliding between tiles) - only when inventory closed
        if moving and not inventory.is_open:
            if direction == "up":
                player_y -= PLAYER_SPEED
                if player_y % TILE_SIZE == 0:
                    moving = False
                    player_y_grid -= 1
            elif direction == "down":
                player_y += PLAYER_SPEED
                if player_y % TILE_SIZE == 0:
                    moving = False
                    player_y_grid += 1
            elif direction == "left":
                player_x -= PLAYER_SPEED
                if player_x % TILE_SIZE == 0:
                    moving = False
                    player_x_grid -= 1
            elif direction == "right":
                player_x += PLAYER_SPEED
                if player_x % TILE_SIZE == 0:
                    moving = False
                    player_x_grid += 1
            
            # When movement completes, check for random encounter
            if not moving:
                if random.random() < ENCOUNTER_CHANCE:
                    return ("RANDOM_BATTLE", inventory)
        
        # Check for Battle Trigger (special tile)
        if player_x_grid == target_x_grid and player_y_grid == target_y_grid and not moving:
            return ("START_BATTLE", inventory)
        
        # Draw Everything
        # Draw grass pattern
        for gx in range(0, WIDTH, TILE_SIZE):
            for gy in range(0, HEIGHT, TILE_SIZE):
                if (gx//TILE_SIZE + gy//TILE_SIZE) % 2 == 0:
                    pygame.draw.rect(screen, (44, 149, 44), (gx, gy, TILE_SIZE, TILE_SIZE))
        
        # Draw battle trigger tile (red = special battle spot)
        pygame.draw.rect(screen, (200, 50, 50), (target_x_grid*TILE_SIZE, target_y_grid*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        # Draw player
        pygame.draw.rect(screen, (50, 100, 200), (player_x, player_y, TILE_SIZE, TILE_SIZE))
        
        # Draw UI text
        font = pygame.font.Font(None, 24)
        text = font.render("Press SPACE to test battle, E for inventory", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        # Draw inventory (if open)
        inventory.draw(screen)
        
        pygame.display.update()