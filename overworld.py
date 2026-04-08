import pygame
import random
import sys
import os
import json

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))
from inventory import InventorySystem
from npc import NPC
<<<<<<< HEAD
from Tiledmap import TiledMap 
=======
from tilemap import build_cave_map
from loader import blit_letterboxed
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

def run_overworld(screen, inventory=None, player_state=None, boss1defeated=False):
    # --- 1. Resolution & Zoom Setup ---
    REAL_WIDTH, REAL_HEIGHT = screen.get_size()
    ZOOM = 2  
    VIRTUAL_WIDTH = REAL_WIDTH // ZOOM
    VIRTUAL_HEIGHT = REAL_HEIGHT // ZOOM
    virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

<<<<<<< HEAD
=======
# Define a larger world so the camera has room to scroll
WORLD_COLS = 100
WORLD_ROWS = 100
WORLD_WIDTH = WORLD_COLS * TILE_SIZE
WORLD_HEIGHT = WORLD_ROWS * TILE_SIZE

# Random encounter settings
ENCOUNTER_CHANCE = 0




def run_overworld(real_screen, inventory=None, player_state=None):
    # logical surface — all drawing happens here at 640x480
    logical = pygame.Surface((WIDTH, HEIGHT))

    # --- Create or use existing inventory ---
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
    if inventory is None:
        inventory = InventorySystem(REAL_WIDTH, REAL_HEIGHT)

    # --- 2. Load the Tiled Map ---
    map_manager = TiledMap(os.path.join("py", "assets", "maps", "cave_level.tmx"))
    map_image = map_manager.make_map()
    
    WORLD_WIDTH = map_manager.width
    WORLD_HEIGHT = map_manager.height
    TILE_SIZE = 32 

    # --- 3. Load JSON Data (Enemies & Items) ---
    json_dir = os.path.join("py", "assets", "jason")
    
    # Load Enemy Data
    try:
        with open(os.path.join(json_dir, "enemies.json"), 'r') as f:
            all_enemy_data = json.load(f)
    except Exception as e:
        print(f"Warning: Could not find enemies.json: {e}")
        all_enemy_data = {}

    # Load Item Data for Chests
    try:
        with open(os.path.join(json_dir, "items.json"), 'r') as f:
            all_item_data = json.load(f)
    except Exception as e:
        print(f"Warning: Could not find items.json: {e}")
        all_item_data = {}

    # --- 4. Extract Objects (NPCs, Enemies, Chests) ---
    npc_list = []
    enemy_list = []
    chests = []

    # Initialize opened_chests set if it doesn't exist
    if not hasattr(player_state, 'opened_chests'):
        player_state.opened_chests = set()

    try:
        entity_layer = map_manager.tmxdata.get_layer_by_name("Entities")
        
        for obj in entity_layer:
            gx, gy = int(obj.x // TILE_SIZE), int(obj.y // TILE_SIZE)
            obj_type = getattr(obj, 'class', getattr(obj, 'type', ""))

            # Handle NPCs
            if obj_type == "NPC":
                raw_dialogue = obj.properties.get("dialogue", "Hello!")
                dialogue_list = raw_dialogue.split('|') 
                new_npc = NPC(obj.name or "Villager", gx, gy, dialogue_list, TILE_SIZE)
                npc_list.append(new_npc)
                
            # Handle Enemies
            elif obj_type == "Enemy":
                enemy_stats = all_enemy_data.get(obj.name, {})
                enemy_list.append({
                    "grid_x": gx, 
                    "grid_y": gy, 
                    "name": obj.name,
                    "hp": enemy_stats.get("hp", 100),
                    "at": enemy_stats.get("attack", 10)
                })

            # Handle Chests
            elif obj_type == "Chest" and obj.id not in player_state.opened_chests:
                item_name = obj.properties.get("item_name", "Basic Health Potion")
                # Pull data from items.json
                item_info = all_item_data.get(item_name, {})
                
                chests.append({
                    "id": obj.id,
                    "x": gx,
                    "y": gy,
                    "name": item_name,
                    "type": item_info.get("type", "misc"),
                    "desc": item_info.get("description", "A mysterious item."),
                    "val": item_info.get("value", 0)
                })
    except Exception as e:
        print(f"Warning: Entity layer processing error: {e}")

    # --- 5. Player & Camera Setup ---
    if player_state is not None:
        player_x_grid, player_y_grid = player_state.x, player_state.y
    else:
        player_x_grid, player_y_grid = 2, 2 
    
    player_x, player_y = player_x_grid * TILE_SIZE, player_y_grid * TILE_SIZE
    moving = False
    PLAYER_SPEED = 2 
    camera_x, camera_y = 0, 0

<<<<<<< HEAD
    # --- Assets ---
    kim_path = os.path.join("py", "assets", "img", "kim-forward.png")
    player_sprite = pygame.transform.scale(pygame.image.load(kim_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
    
    vivi_path = os.path.join("py", "assets", "img", "vivi-right.png")
    base_npc_img = pygame.image.load(vivi_path).convert_alpha()
    npc_sprite = pygame.transform.scale(base_npc_img, (TILE_SIZE, TILE_SIZE))
    
    # Tinted variants for Enemies and Chests
    enemy_sprite = npc_sprite.copy()
    enemy_sprite.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
    
    chest_sprite = npc_sprite.copy()
    chest_sprite.fill((255, 255, 100), special_flags=pygame.BLEND_RGB_MULT)

    # --- Helper Functions ---
    def get_collisions():
        current_collisions = list(map_manager.collisions)
        for npc in npc_list:
            current_collisions.append(pygame.Rect(npc.grid_x * TILE_SIZE, npc.grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        # Note: We don't add chests to collisions so the player can walk ONTO them to open them.
        return current_collisions

    def clamp_camera(px, py):
        cam_x = max(0, min(px + TILE_SIZE // 2 - VIRTUAL_WIDTH // 2, WORLD_WIDTH - VIRTUAL_WIDTH))
        cam_y = max(0, min(py + TILE_SIZE // 2 - VIRTUAL_HEIGHT // 2, WORLD_HEIGHT - VIRTUAL_HEIGHT))
        return cam_x, cam_y

    def draw_dialogue_box(screen, text):
        # Box dimensions
        box_rect = pygame.Rect(50, REAL_HEIGHT - 150, REAL_WIDTH - 100, 120)
        pygame.draw.rect(screen, (0, 0, 0), box_rect) # Black background
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3) # White border
        
        # Text rendering
        font = pygame.font.SysFont("Arial", 24)
        text_surf = font.render(text, True, (255, 255, 255))
        screen.blit(text_surf, (box_rect.x + 20, box_rect.y + 20))
    
    clock = pygame.time.Clock()
    # --- Main Loop ---
    while True:
        clock.tick(60)
=======
    target_x_grid = player_state.get('target_x_grid', player_x_grid + 5) if player_state else player_x_grid + 5
    target_y_grid = player_state.get('target_y_grid', player_y_grid) if player_state else player_y_grid

    tile_grid, collision_tiles = build_cave_map(WORLD_COLS, WORLD_ROWS)

    npc_list = [
        NPC("John", 53, 48, ["SUP dude", "There are many enemies here!", "Watch out for the red tiles!"], TILE_SIZE)
    ]

    active_npc = None

    for npc in npc_list:
        collision_tiles.add((npc.grid_x, npc.grid_y))

    def build_state():
        return {
            'player_x_grid': player_x_grid,
            'player_y_grid': player_y_grid,
            'player_x': player_x,
            'player_y': player_y,
            'direction': direction,
            'camera_x': camera_x,
            'camera_y': camera_y,
            'target_x_grid': target_x_grid,
            'target_y_grid': target_y_grid,
        }

    def clamp_camera(px, py):
        half_tile = TILE_SIZE // 2
        cam_x = int(px + half_tile - WIDTH // 2)
        cam_y = int(py + half_tile - HEIGHT // 2)
        max_cam_x = max(0, WORLD_WIDTH - WIDTH)
        max_cam_y = max(0, WORLD_HEIGHT - HEIGHT)
        cam_x = max(0, min(max_cam_x, cam_x))
        cam_y = max(0, min(max_cam_y, cam_y))
        return cam_x, cam_y

    target_x_grid = min(WORLD_COLS - 1, max(0, target_x_grid))
    target_y_grid = min(WORLD_ROWS - 1, max(0, target_y_grid))
    camera_x, camera_y = clamp_camera(player_x, player_y)

    clock = pygame.time.Clock()

    def load_tile(path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (size, size))
        except Exception:
            return None

    tile_floor     = load_tile(os.path.join("assets", "img", "limestone_floor.png"), TILE_SIZE)
    tile_wall      = load_tile(os.path.join("assets", "img", "Stone_wall.png"), TILE_SIZE)
    tile_edge      = load_tile(os.path.join("assets", "img", "Stone_frame.png"), TILE_SIZE)
    tile_lime_edge = load_tile(os.path.join("assets", "img", "Limestone_frame.png"), TILE_SIZE)

    player_sprite = None
    possible_paths = [
        os.path.join("assets", "img", "kim-forward.png"),
        os.path.join("assets", "img", "player.png"),
        os.path.join("assets/img", "player.png"),
        os.path.join(os.path.dirname(__file__), "img", "player.png")
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

        # Block of code for handling movement
        if not moving and not inventory.is_open:
            nextx, nexty = player_x_grid, player_y_grid
            potential_direction = None
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT]:
                PLAYER_SPEED = 4
            else:
                PLAYER_SPEED = 2

            if keys[pygame.K_LEFT] and player_x_grid > 0:
                potential_direction = "left"
                nextx -= 1
            elif keys[pygame.K_RIGHT] and player_x_grid < WORLD_COLS - 1:
                potential_direction = "right"
                nextx += 1
            elif keys[pygame.K_UP] and player_y_grid > 0:
                potential_direction = "up"
                nexty -= 1
            elif keys[pygame.K_DOWN] and player_y_grid < WORLD_ROWS - 1:
                potential_direction = "down"
                nexty += 1

            if potential_direction:
                if (nextx, nexty) not in collision_tiles:
                    direction = potential_direction
                    moving = True
                else:
                    print(f"Bumped into a wall at {nextx}, {nexty} facing {potential_direction}")

>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape pressed")
                    return ("MENU", inventory, player_state)

<<<<<<< HEAD
                if event.key == pygame.K_SPACE:
                    # 1. Is anyone currently talking?
                    active_npc = next((n for n in npc_list if n.is_talking), None)
                    
=======
            if inventory.handle_event(event):
                continue

            if event.type == pygame.KEYDOWN and not moving and not inventory.is_open:

<<<<<<< HEAD
                nextx, nexty = player_x_grid, player_y_grid
                potential_direction = None
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT]:
                    PLAYER_SPEED = 4
                else:
                    PLAYER_SPEED = 2

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
                    if (nextx, nexty) not in collision_tiles:
                        direction = potential_direction
                        moving = True
                    else:
                        print(f"Bumped into a wall at {nextx}, {nexty} facing {potential_direction}")

                elif event.key == pygame.K_SPACE:
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
=======
                if event.key == pygame.K_SPACE:
>>>>>>> fa1cda7 (fixed continuous movement causing problems)
                    if active_npc:
                        # 2. If yes, try to go to the next line
                        if not active_npc.advance_dialogue():
<<<<<<< HEAD
                            # If advance_dialogue returns False, the chat is over
                            active_npc.is_talking = False 
                            print("Finished talking.")
                    else:
                        # 3. If no one is talking, check for a nearby NPC to start
=======
                            active_npc = None
                    else:
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
                        for npc in npc_list:
                            dx = abs(player_x_grid - npc.grid_x)
                            dy = abs(player_y_grid - npc.grid_y)
                            if dx + dy == 1:
                                npc.is_talking = True
<<<<<<< HEAD
            
            inventory.handle_event(event, player_state)
        
        # Make sure player can't move while the dialogue is active
        current_dialogue_active = any(npc.is_talking for npc in npc_list)
        keys = pygame.key.get_pressed()
        if not moving and not inventory.is_open and not current_dialogue_active:
            next_gx, next_gy = player_x_grid, player_y_grid
            moved = False
            if keys[pygame.K_a]: next_gx -= 1; moved = True
            elif keys[pygame.K_d]: next_gx += 1; moved = True
            elif keys[pygame.K_w]: next_gy -= 1; moved = True
            elif keys[pygame.K_s]: next_gy += 1; moved = True

            if moved:
                target_rect = pygame.Rect(next_gx * TILE_SIZE, next_gy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if target_rect.collidelist(get_collisions()) == -1:
                    player_x_grid, player_y_grid = next_gx, next_gy
                    moving = True

        if moving:
            target_px, target_py = player_x_grid * TILE_SIZE, player_y_grid * TILE_SIZE
            if player_x < target_px: player_x += PLAYER_SPEED
            elif player_x > target_px: player_x -= PLAYER_SPEED
            if player_y < target_py: player_y += PLAYER_SPEED
            elif player_y > target_py: player_y -= PLAYER_SPEED

            # When the movement animation finishes
            if player_x == target_px and player_y == target_py:
                moving = False
                
                # Update player state coordinates
                player_state.x, player_state.y = player_x_grid, player_y_grid

                # Check for Enemy encounters
                for enemy in enemy_list:
                    if player_x_grid == enemy["grid_x"] and player_y_grid == enemy["grid_y"]:
                        player_state.last_enemy_name = enemy["name"]
                        return ("START_BATTLE", inventory, player_state)

                # Check for Chest loot
                for chest in chests[:]:
                    if player_x_grid == chest["x"] and player_y_grid == chest["y"]:
                        # inventory.add_item uses [Name, Type, Desc, Value]
                        inventory.add_item([
                            chest["name"], 
                            chest["type"], 
                            chest["desc"], 
                            chest["val"]
                        ])
                        player_state.opened_chests.add(chest["id"])
                        chests.remove(chest)
                        print(f"Obtained {chest['name']}!")

        camera_x, camera_y = clamp_camera(player_x, player_y)

        # --- Drawing ---
        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(map_image, (-camera_x, -camera_y))
        
        for npc in npc_list:
            virtual_surface.blit(npc_sprite, (npc.grid_x * TILE_SIZE - camera_x, npc.grid_y * TILE_SIZE - camera_y))
        
        for enemy in enemy_list:
            virtual_surface.blit(enemy_sprite, (enemy["grid_x"] * TILE_SIZE - camera_x, enemy["grid_y"] * TILE_SIZE - camera_y))
        
        for chest in chests:
            virtual_surface.blit(chest_sprite, (chest["x"] * TILE_SIZE - camera_x, chest["y"] * TILE_SIZE - camera_y))

        virtual_surface.blit(player_sprite, (player_x - camera_x, player_y - camera_y))

        # Scale up and Blit to real screen
        scaled_surface = pygame.transform.scale(virtual_surface, (REAL_WIDTH, REAL_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        
        # Draw Inventory Overlay (Pass player_state to fix the crash)
        if inventory.is_open: 
            inventory.draw(screen, player_state)
        
        # NPC DIALOGUE
        for npc in npc_list:
            if npc.is_talking:
                draw_dialogue_box(screen, npc.get_current_line())
=======
                                active_npc = npc
                                break

        inventory.update()

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

            if not moving:
                if random.random() < ENCOUNTER_CHANCE:
                    return ("RANDOM_BATTLE", inventory, build_state())

                if player_x_grid == target_x_grid and player_y_grid == target_y_grid:
                    return ("START_BATTLE", inventory, build_state())

        camera_x, camera_y = clamp_camera(player_x, player_y)

        # --- Draw everything to logical surface ---
        logical.fill((26, 28, 44))

        start_col = max(0, camera_x // TILE_SIZE)
        end_col   = min(WORLD_COLS, (camera_x + WIDTH) // TILE_SIZE + 2)
        start_row = max(0, camera_y // TILE_SIZE)
        end_row   = min(WORLD_ROWS, (camera_y + HEIGHT) // TILE_SIZE + 2)

        tile_images = {
            0: tile_floor,
            1: tile_wall,
            2: tile_edge,
            3: None,  # VOID
        }

        for gx in range(start_col, end_col):
            for gy in range(start_row, end_row):
                tile_id = tile_grid[gx][gy]
                img = tile_images.get(tile_id)
                sx = gx * TILE_SIZE - camera_x
                sy = gy * TILE_SIZE - camera_y
                if img:
                    logical.blit(img, (sx, sy))

        # Battle trigger tile (red)
        target_screen_x = target_x_grid * TILE_SIZE - camera_x
        target_screen_y = target_y_grid * TILE_SIZE - camera_y
        pygame.draw.rect(logical, (200, 50, 50),
                         (target_screen_x, target_screen_y, TILE_SIZE, TILE_SIZE))

        # NPCs
        for npc in npc_list:
            npc_screen_x = npc.grid_x * TILE_SIZE - camera_x
            npc_screen_y = npc.grid_y * TILE_SIZE - camera_y
            logical.blit(npc.image, (npc_screen_x, npc_screen_y))

        # Dialogue box
        if active_npc and active_npc.is_talking:
            box_rect = pygame.Rect(20, HEIGHT - 120, WIDTH - 40, 100)
            pygame.draw.rect(logical, (20, 20, 40), box_rect, border_radius=8)
            pygame.draw.rect(logical, (255, 255, 255), box_rect, width=2, border_radius=8)

            font = pygame.font.Font(None, 28)
            name_surf = font.render(active_npc.name, True, (255, 220, 100))
            logical.blit(name_surf, (box_rect.x + 12, box_rect.y + 10))

            line_surf = font.render(active_npc.get_current_line(), True, (255, 255, 255))
            logical.blit(line_surf, (box_rect.x + 12, box_rect.y + 40))

            small_font = pygame.font.Font(None, 20)
            prompt = small_font.render("SPACE to continue...", True, (150, 150, 150))
            logical.blit(prompt, (box_rect.x + 12, box_rect.y + 72))

        # Player
        player_screen_x = player_x - camera_x
        player_screen_y = player_y - camera_y
        if player_sprite:
            logical.blit(player_sprite, (player_screen_x, player_screen_y))
        else:
            pygame.draw.rect(logical, (50, 100, 200),
                             (player_screen_x, player_screen_y, TILE_SIZE, TILE_SIZE))

        # UI text
        ui_font = pygame.font.Font(None, 24)
        text = ui_font.render("E for inventory", True, (255, 255, 255))
        logical.blit(text, (10, 10))

        # Inventory (draws to logical)
        inventory.draw(logical)
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)

        # Scale logical → real window with letterboxing
        blit_letterboxed(logical, real_screen)
        pygame.display.update()
