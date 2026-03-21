import pygame
import random
import sys
import os

# Add py folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'py'))
from inventory import InventorySystem

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

def run_overworld(screen, inventory=None, player_state=None):
    """Run the overworld screen.
    Args:
        screen: The pygame display surface
        inventory: Optional InventorySystem instance. If None, creates a new one.
        player_state: Optional dict with player position/direction/camera
    Returns:
        Tuple of (action_string, inventory, player_state)
    """
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

    # Store the initial target position so it doesn't drift each re-entry.
    # Only set it once based on the ORIGINAL spawn, not the restored position.
    target_x_grid = player_state.get('target_x_grid', player_x_grid + 5) if player_state else player_x_grid + 5
    target_y_grid = player_state.get('target_y_grid', player_y_grid) if player_state else player_y_grid

    def build_state():
        """Helper: pack all local vars into a state dict to return."""
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
        """Center camera on the player while staying inside world bounds."""
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

    # --- Load player sprite once (falls back to a rectangle if not found) ---
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
        screen.fill((34, 139, 34))  # Grass green BG

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return ("QUIT", inventory, build_state())

            # Let inventory handle its events first
            if inventory.handle_event(event):
                continue  # Event was consumed by inventory

            # Grid Movement Input (only when inventory is closed)
            if event.type == pygame.KEYDOWN and not moving and not inventory.is_open:
                if event.key == pygame.K_LEFT and player_x_grid > 0:
                    moving, direction = True, "left"
                elif event.key == pygame.K_RIGHT and player_x_grid < WORLD_COLS - 1:
                    moving, direction = True, "right"
                elif event.key == pygame.K_UP and player_y_grid > 0:
                    moving, direction = True, "up"
                elif event.key == pygame.K_DOWN and player_y_grid < WORLD_ROWS - 1:
                    moving, direction = True, "down"
                elif event.key == pygame.K_a and player_x_grid > 0:
                    moving, direction = True, "left"
                elif event.key == pygame.K_d and player_x_grid < WORLD_COLS - 1:
                    moving, direction = True, "right"
                elif event.key == pygame.K_w and player_y_grid > 0:
                    moving, direction = True, "up"
                elif event.key == pygame.K_s and player_y_grid < WORLD_ROWS - 1:
                    moving, direction = True, "down"

                # TEST: Press SPACE to force a battle
                elif event.key == pygame.K_SPACE:
                    return ("RANDOM_BATTLE", inventory, build_state())

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
                    return ("RANDOM_BATTLE", inventory, build_state())

        # Update camera each frame
        camera_x, camera_y = clamp_camera(player_x, player_y)

        # Check for Battle Trigger (special tile)
        if player_x_grid == target_x_grid and player_y_grid == target_y_grid and not moving:
            return ("START_BATTLE", inventory, build_state())

        # Draw Everything
        # Draw grass pattern (only tiles visible in the current camera view)
        start_col = max(0, camera_x // TILE_SIZE)
        end_col = min(WORLD_COLS, (camera_x + WIDTH) // TILE_SIZE + 2)
        start_row = max(0, camera_y // TILE_SIZE)
        end_row = min(WORLD_ROWS, (camera_y + HEIGHT) // TILE_SIZE + 2)
        for gx in range(start_col, end_col):
            for gy in range(start_row, end_row):
                if (gx + gy) % 2 == 0:
                    screen_x = gx * TILE_SIZE - camera_x
                    screen_y = gy * TILE_SIZE - camera_y
                    pygame.draw.rect(
                        screen,
                        (44, 149, 44),
                        (screen_x, screen_y, TILE_SIZE, TILE_SIZE)
                    )

        # Draw battle trigger tile (red = special battle spot)
        target_screen_x = target_x_grid * TILE_SIZE - camera_x
        target_screen_y = target_y_grid * TILE_SIZE - camera_y
        pygame.draw.rect(
            screen,
            (200, 50, 50),
            (target_screen_x, target_screen_y, TILE_SIZE, TILE_SIZE)
        )

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
        text = font.render("Press SPACE to test battle, E for inventory", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        # Draw inventory (if open)
        inventory.draw(screen)

        pygame.display.update()