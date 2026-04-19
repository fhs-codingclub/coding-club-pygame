import pygame
import random
import sys
import os
import json # Added for JSON support

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))
from inventory import InventorySystem
from npc import NPC
from Tiledmap import TiledMap 

def run_overworld(screen, inventory=None, player_state=None, boss1defeated=False):
    # --- 1. Resolution & Zoom Setup ---
    REAL_WIDTH, REAL_HEIGHT = screen.get_size()
    ZOOM = 2  
    VIRTUAL_WIDTH = REAL_WIDTH // ZOOM
    VIRTUAL_HEIGHT = REAL_HEIGHT // ZOOM
    virtual_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

    if inventory is None:
        inventory = InventorySystem(REAL_WIDTH, REAL_HEIGHT)

    # --- 2. Load the Tiled Map ---
    map_manager = TiledMap(os.path.join("py", "assets", "maps", "cave_level.tmx"))
    map_image = map_manager.make_map()
    
    WORLD_WIDTH = map_manager.width
    WORLD_HEIGHT = map_manager.height
    TILE_SIZE = 32 

    # --- 3. Load Enemy JSON Data ---
    json_path = os.path.join("py", "assets", "jason", "enemies.json")
    try:
        with open(json_path, 'r') as f:
            all_enemy_data = json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find {json_path}. Using empty data.")
        all_enemy_data = {}

    # --- 4. Extract Objects ---
    npc_list = []
    enemy_list = []

    try:
        entity_layer = map_manager.tmxdata.get_layer_by_name("Entities")
        
        for obj in entity_layer:
            gx, gy = int(obj.x // TILE_SIZE), int(obj.y // TILE_SIZE)
            obj_type = getattr(obj, 'class', getattr(obj, 'type', ""))

            if obj_type == "NPC":
                dialogue = obj.properties.get("dialogue", "Hello!")
                new_npc = NPC(obj.name or "Villager", gx, gy, [dialogue], TILE_SIZE)
                npc_list.append(new_npc)
                
            elif obj_type == "Enemy":
                # Check if this enemy exists in our JSON
                enemy_stats = all_enemy_data.get(obj.name)
                
                if enemy_stats:
                    enemy_list.append({
                        "grid_x": gx, 
                        "grid_y": gy, 
                        "name": obj.name,
                        "hp": enemy_stats.get("hp", 100),
                        "at": enemy_stats.get("attack", 10),
                        "image": enemy_stats.get("image", "placeholder.png")
                    })
                else:
                    # Fallback if enemy isn't in JSON
                    print(f"Warning: {obj.name} not found in enemies.json")
                    enemy_list.append({
                        "grid_x": gx, "grid_y": gy, "name": obj.name or "Unknown"
                    })
    except (ValueError, AttributeError):
        print("Warning: No 'Entities' layer found in Tiled.")

    # --- 5. Player Setup ---
    if player_state is not None:
        player_x_grid, player_y_grid = player_state.x, player_state.y
    else:
        player_x_grid, player_y_grid = 2, 2 
    
    player_x, player_y = player_x_grid * TILE_SIZE, player_y_grid * TILE_SIZE
    moving = False
    PLAYER_SPEED = 2 
    camera_x, camera_y = 0, 0

    # --- Assets ---
    kim_path = os.path.join("py", "assets", "img", "kim-forward.png")
    player_sprite = pygame.transform.scale(pygame.image.load(kim_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
    vivi_path = os.path.join("py", "assets", "img", "vivi-right.png")
    npc_sprite = pygame.transform.scale(pygame.image.load(vivi_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
    
    enemy_sprite = npc_sprite.copy()
    enemy_sprite.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)

    def get_collisions():
        current_collisions = list(map_manager.collisions)
        for npc in npc_list:
            current_collisions.append(pygame.Rect(npc.grid_x * TILE_SIZE, npc.grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return current_collisions

    def clamp_camera(px, py):
        cam_x = max(0, min(px + TILE_SIZE // 2 - VIRTUAL_WIDTH // 2, WORLD_WIDTH - VIRTUAL_WIDTH))
        cam_y = max(0, min(py + TILE_SIZE // 2 - VIRTUAL_HEIGHT // 2, WORLD_HEIGHT - VIRTUAL_HEIGHT))
        return cam_x, cam_y

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return ("QUIT", inventory, player_state)
            inventory.handle_event(event, player_state)

        keys = pygame.key.get_pressed()
        if not moving and not inventory.is_open:
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

            if player_x == target_px and player_y == target_py:
                moving = False
                for enemy in enemy_list:
                    if player_x_grid == enemy["grid_x"] and player_y_grid == enemy["grid_y"]:
                        # Pass the full name for the JSON lookup in the battle system
                        player_state.last_enemy_name = enemy["name"]
                        return ("START_BATTLE", inventory, player_state)

        camera_x, camera_y = clamp_camera(player_x, player_y)

        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(map_image, (-camera_x, -camera_y))
        for npc in npc_list:
            virtual_surface.blit(npc_sprite, (npc.grid_x * TILE_SIZE - camera_x, npc.grid_y * TILE_SIZE - camera_y))
        for enemy in enemy_list:
            virtual_surface.blit(enemy_sprite, (enemy["grid_x"] * TILE_SIZE - camera_x, enemy["grid_y"] * TILE_SIZE - camera_y))
        virtual_surface.blit(player_sprite, (player_x - camera_x, player_y - camera_y))

        scaled_surface = pygame.transform.scale(virtual_surface, (REAL_WIDTH, REAL_HEIGHT))
        screen.blit(scaled_surface, (0, 0))
        if inventory.is_open: inventory.draw(screen)
        pygame.display.update()