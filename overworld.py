import pygame
import random
import sys
import os

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))
from inventory import InventorySystem
from npc import NPC
from tilemap import build_cave_map

WIDTH = 640
HEIGHT = 480
TILE_SIZE = 48

# Define a larger world so the camera has room to scroll
WORLD_COLS = 100
WORLD_ROWS = 100
WORLD_WIDTH = WORLD_COLS * TILE_SIZE
WORLD_HEIGHT = WORLD_ROWS * TILE_SIZE

# Random encounter settings
ENCOUNTER_CHANCE = 0  

def run_overworld(screen, inventory=None, player_state=None, boss1defeated=False):
    # --- Create or use existing inventory ---
    if inventory is None:
        inventory = InventorySystem(WIDTH, HEIGHT)

    # --- Local Settings ---
    if player_state is not None:
        player_x_grid = player_state.x 
        player_y_grid = player_state.y
        player_x = player_x_grid * TILE_SIZE
        player_y = player_y_grid * TILE_SIZE
        direction = None
        camera_x = 0
        camera_y = 0
    else:
        player_x_grid = WORLD_COLS // 2
        player_y_grid = WORLD_ROWS // 2
        player_x = player_x_grid * TILE_SIZE
        player_y = player_y_grid * TILE_SIZE
        direction = None
        camera_x = 0
        camera_y = 0

    moving = False
    PLAYER_SPEED = 2

    # Store the initial target position so it doesn't drift each re-entry.
    # Only set it once based on the ORIGINAL spawn, not the restored position.
    target_x_grid = 60
    target_y_grid = 50

    # LOL its hardcoded rn but idc use for loops or wtv to make walls and stuff later, I kinda just wanted to test the battle trigger so I threw this together real quick
    tile_grid, collision_tiles = build_cave_map(WORLD_COLS, WORLD_ROWS)

    npc_list = [
        NPC("John", 53, 48, ["SUP dude", "There are many enemies here!", "Watch out for the red tiles!"], TILE_SIZE)
    ]  # NPC implementation

    # Define chests: [grid_x, grid_y, item_name, is_collected]
    chests = [
        [52, 50, "Basic Health Potion", False] 
    ]

    active_npc = None  # Track which NPC we're currently talking to

    #Add npc's to collision tiles so player can't walk through them
    for npc in npc_list:
        collision_tiles.add((npc.grid_x, npc.grid_y))

    def build_state():
        player_state.x = player_x_grid
        player_state.y = player_y_grid
        return player_state

    def clamp_camera(px, py):
        
        half_tile = TILE_SIZE // 2
        cam_x = int(px + half_tile - WIDTH // 2)
        cam_y = int(py + half_tile - HEIGHT // 2)
        max_cam_x = max(0, WORLD_WIDTH - WIDTH)
        max_cam_y = max(0, WORLD_HEIGHT - HEIGHT)
        cam_x = max(0, min(max_cam_x, cam_x))
        cam_y = max(0, min(max_cam_y, cam_y))
        return cam_x, cam_y

    # Ensure target stays in bounds
    target_x_grid = min(WORLD_COLS - 1, max(0, target_x_grid))
    target_y_grid = min(WORLD_ROWS - 1, max(0, target_y_grid))
    camera_x, camera_y = clamp_camera(player_x, player_y)

    clock = pygame.time.Clock()

    #Load Tile assets
    def load_tile(path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (size, size))
        except Exception:
            return None
    
    tile_floor  = load_tile(os.path.join("py", "assets","img", "limestone_floor.png"), TILE_SIZE)
    tile_wall   = load_tile(os.path.join("py", "assets", "img", "Stone_wall.png"), TILE_SIZE)
    tile_edge   = load_tile(os.path.join("py", "assets", "img", "Stone_frame.png"), TILE_SIZE)
    tile_lime_edge = load_tile(os.path.join("py", "assets", "img", "Limestone_frame.png"), TILE_SIZE)

    # --- Load player sprite once (falls back to a rectangle if not found) ---
    player_sprite = None
    possible_paths = [
        os.path.join("py", "assets", "img", "kim-forward.png"),
        os.path.join("py", "assets", "img", "player.png"),
        os.path.join("py", "assets", "img", "player.png"),
        os.path.join(os.path.dirname(__file__), "py", "assets", "img", "player.png")
    ]
    for p in possible_paths:
        try:
            if os.path.exists(p):
                tmp = pygame.image.load(p).convert_alpha()
                player_sprite = pygame.transform.scale(tmp, (TILE_SIZE, TILE_SIZE))
                break
        except Exception:
            player_sprite = None

    while True:
        clock.tick(60)
        screen.fill((26, 28, 44))  # Background for academia cave dark grey

        DOOR_X, DOOR_Y = 60, 55    #Door to leave area

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("QUIT", inventory, build_state())

            # Let inventory handle its events first
            if inventory.handle_event(event, player_state):
                continue  # Event was consumed by inventory

            # Grid Movement Input (only when inventory is closed)
            if event.type == pygame.KEYDOWN and not moving and not inventory.is_open:

                nextx, nexty = player_x_grid, player_y_grid
                potential_direction = None
                     
                if event.key == pygame.K_LEFT and player_x_grid > 0:
                    potential_direction = "left"
                    nextx -= 1
                elif event.key == pygame.K_RIGHT and player_x_grid < WORLD_COLS - 1:
                    potential_direction = "right"
                    nextx += 1
                elif event.key == pygame.K_UP and player_y_grid > 0:
                    potential_direction = "up"
                    nexty -= 1
                elif event.key == pygame.K_DOWN and player_y_grid < WORLD_ROWS - 1:
                    potential_direction = "down"
                    nexty += 1
                elif event.key == pygame.K_a and player_x_grid > 0:
                    potential_direction = "left"
                    nextx -= 1
                elif event.key == pygame.K_d and player_x_grid < WORLD_COLS - 1:
                    potential_direction = "right"
                    nextx += 1
                elif event.key == pygame.K_w and player_y_grid > 0:
                    potential_direction = "up"
                    nexty -= 1
                elif event.key == pygame.K_s and player_y_grid < WORLD_ROWS - 1:
                    potential_direction = "down"
                    nexty += 1

                if potential_direction:
                    if nextx == DOOR_X and nexty == DOOR_Y :
                        if boss1defeated:
                            direction = potential_direction
                            moving = True
                        else:
                            print("The door is locked. Defeat the boss to open it!")
                            moving = False
                    elif (nextx, nexty) not in collision_tiles:
                        direction = potential_direction
                        moving = True
                    else:
                        print("Bumped into a wall at", nextx, nexty, "facing", potential_direction)
                        moving = False
                
                elif event.key == pygame.K_SPACE:
                    if active_npc:
                        if not active_npc.advance_dialogue():
                            active_npc = None
                    else: 
                        for npc in npc_list:
                            if abs(player_x_grid - npc.grid_x) <= 1 and abs(player_y_grid - npc.grid_y) <= 1:
                                npc.is_talking = True
                                active_npc = npc
                                break
        

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
                if player_x_grid == DOOR_X and player_y_grid == DOOR_Y:
                    return ("WIN_GAME", inventory, build_state())
                
                if random.random() < ENCOUNTER_CHANCE:
                    return ("RANDOM_BATTLE", inventory, build_state())
                
            # Check for battle trigger tile (red tile)
                if player_x_grid == target_x_grid and player_y_grid == target_y_grid:
                    return ("START_BATTLE", inventory, build_state())

        # Update camera each frame
        camera_x, camera_y = clamp_camera(player_x, player_y)

        # Draw Everything
        # Draw Tile Pattern
        start_col = max(0, camera_x // TILE_SIZE)
        end_col = min(WORLD_COLS, (camera_x + WIDTH) // TILE_SIZE + 2)
        start_row = max(0, camera_y // TILE_SIZE)
        end_row = min(WORLD_ROWS, (camera_y + HEIGHT) // TILE_SIZE + 2)
        
        tile_images = {
            0: tile_floor,
            1: tile_wall,
            2: tile_edge,
            3: None,  # VOID = just background color
        }

        for gx in range(start_col, end_col):
            for gy in range(start_row, end_row):
                tile_id = tile_grid[gx][gy]
                img = tile_images.get(tile_id)
                sx = gx * TILE_SIZE - camera_x
                sy = gy * TILE_SIZE - camera_y
                if img:
                    screen.blit(img, (sx, sy))

        # VOID tiles just show the dark background, no blit needed
        # Draw battle trigger tile (red = special battle spot)
        target_screen_x = target_x_grid * TILE_SIZE - camera_x
        target_screen_y = target_y_grid * TILE_SIZE - camera_y
        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (target_screen_x, target_screen_y, TILE_SIZE, TILE_SIZE)
        )
        
        # --- Draw and Handle Chests ---
        for chest in chests:
            gx, gy, item_name, collected = chest
            if not collected:
                # 1. Calculate where it goes on the screen
                chest_sx = gx * TILE_SIZE - camera_x
                chest_sy = gy * TILE_SIZE - camera_y
                
                # 2. Draw it (Gold/Yellow rectangle)
                # You can replace this with a chest sprite later!
                pygame.draw.rect(screen, (255, 215, 0), (chest_sx + 8, chest_sy + 8, 32, 32))
                pygame.draw.rect(screen, (139, 69, 19), (chest_sx + 8, chest_sy + 8, 32, 32), 2) # Brown border
                
                # 3. Check for collision
                if player_x_grid == gx and player_y_grid == gy:
                    chest[3] = True  # Mark as collected so it disappears
                    inventory.add_item_by_name(item_name)
                    print(f"Obtained {item_name}!")

        # Draw NPCs (blue)
        for npc in npc_list:
            npc_screen_x = npc.grid_x * TILE_SIZE - camera_x
            npc_screen_y = npc.grid_y * TILE_SIZE - camera_y
            screen.blit(npc.image, (npc_screen_x, npc_screen_y))

        if active_npc and active_npc.is_talking:
            # Draw dialogue box background
            box_rect = pygame.Rect(20, HEIGHT - 120, WIDTH - 40, 100)
            pygame.draw.rect(screen, (20, 20, 40), box_rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, width=2, border_radius=8)
            
            # Draw NPC name
            font = pygame.font.Font(None, 28)
            name_surf = font.render(active_npc.name, True, (255, 220, 100))
            screen.blit(name_surf, (box_rect.x + 12, box_rect.y + 10))
            
            # Draw current dialogue line
            line_surf = font.render(active_npc.get_current_line(), True, (255, 255, 255))
            screen.blit(line_surf, (box_rect.x + 12, box_rect.y + 40))
            
            # Draw "press space" prompt
            small_font = pygame.font.Font(None, 20)
            prompt = small_font.render("SPACE to continue...", True, (150, 150, 150))
            screen.blit(prompt, (box_rect.x + 12, box_rect.y + 72))

        # Draw door
        door_sx = DOOR_X * TILE_SIZE - camera_x
        door_sy = DOOR_Y * TILE_SIZE - camera_y
        if not boss1defeated:
            # Locked door (Red/Brown)
            pygame.draw.rect(screen, (139, 69, 19), (door_sx, door_sy, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (255, 0, 0), (door_sx+10, door_sy+10, TILE_SIZE-20, TILE_SIZE-20)) # Red lock
        else:
            # Open door (Green/Empty)
            pygame.draw.rect(screen, (34, 139, 34), (door_sx, door_sy, TILE_SIZE, TILE_SIZE))
        
        # Draw player (sprite if available, otherwise fallback rectangle)
        player_screen_x = player_x - camera_x
        player_screen_y = player_y - camera_y
        if player_sprite:
            screen.blit(player_sprite, (player_screen_x, player_screen_y))
        else:
            pygame.draw.rect(
                screen,
                (50, 100, 200),
                (player_screen_x, player_screen_y, TILE_SIZE, TILE_SIZE)
            )

        # Draw UI text
        font = pygame.font.Font(None, 24)
        text = font.render("E for inventory", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Draw inventory (if open)
        inventory.draw(screen, player_state)

        pygame.display.update()