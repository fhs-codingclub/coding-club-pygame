import pygame
import random
import sys
import os
import json

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))
from inventory import InventorySystem
from npc import NPC
from tilemap import build_cave_map
from loader import blit_letterboxed

with open('jason/test.json', 'r') as file:
    data = json.load(file)

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




def run_overworld(real_screen, inventory=None, player_state=None):
    # logical surface — all drawing happens here at 640x480
    logical = pygame.Surface((WIDTH, HEIGHT))

    # --- Create or use existing inventory ---
    if inventory is None:
        inventory = InventorySystem(WIDTH, HEIGHT)

    # --- Local Settings ---
    if player_state is not None:
        player_x_grid = player_state.get('player_x_grid', WORLD_COLS // 2)
        player_y_grid = player_state.get('player_y_grid', WORLD_ROWS // 2)
        player_x = player_state.get('player_x', player_x_grid * TILE_SIZE)
        player_y = player_state.get('player_y', player_y_grid * TILE_SIZE)
        direction = player_state.get('direction', None)
        camera_x = player_state.get('camera_x', 0)
        camera_y = player_state.get('camera_y', 0)
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("QUIT", inventory, build_state())

            if inventory.handle_event(event):
                continue

            if event.type == pygame.KEYDOWN and not moving and not inventory.is_open:

                if event.key == pygame.K_SPACE:
                    if active_npc:
                        if not active_npc.advance_dialogue():
                            active_npc = None
                            # This is for debug, remove before merging with main branch
                            item1 = data["item1"]
                            inventory.add_item(item1)
                    else:
                        for npc in npc_list:
                            if abs(player_x_grid - npc.grid_x) <= 1 and abs(player_y_grid - npc.grid_y) <= 1:
                                npc.is_talking = True
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

        # Scale logical → real window with letterboxing
        blit_letterboxed(logical, real_screen)
        pygame.display.update()