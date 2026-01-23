# THIS IS VIBE CODED!!!! please note that since time is an issue

import pygame
import sys

# --------------------
# CONFIG
# --------------------
WIDTH, HEIGHT = 640, 480
FPS = 60
BLOCK_SIZE = 24
SPIRAL_SPEED = 5  


def run_transition(screen):
    """Run the spiral transition effect. Returns True if completed, False if quit."""
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)

    # --------------------
    # SPIRAL BOUNDS
    # --------------------
    left = 0
    top = 0
    right = WIDTH
    bottom = HEIGHT

    x, y = left, top
    direction = 0  # 0=right, 1=down, 2=left, 3=up
    fade_alpha = 0
    finished = False

    spiral_surface = pygame.Surface((WIDTH, HEIGHT))
    spiral_surface.fill((255, 255, 255))  # white start

    # --------------------
    # TRANSITION LOOP
    # --------------------
    running = True
    transition_complete = False
    
    while running and not transition_complete:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill((255, 255, 255))
        if not finished:
            for _ in range(SPIRAL_SPEED):
                if direction == 0:  # right
                    pygame.draw.rect(
                        spiral_surface, (0, 0, 0),
                        (x, y, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    x += BLOCK_SIZE
                    if x + BLOCK_SIZE >= right:
                        direction = 1
                        top += BLOCK_SIZE
                        x = right - BLOCK_SIZE

                elif direction == 1:  # down
                    pygame.draw.rect(
                        spiral_surface, (0, 0, 0),
                        (x, y, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    y += BLOCK_SIZE
                    if y + BLOCK_SIZE >= bottom:
                        direction = 2
                        right -= BLOCK_SIZE
                        y = bottom - BLOCK_SIZE

                elif direction == 2:  # left
                    pygame.draw.rect(
                        spiral_surface, (0, 0, 0),
                        (x, y, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    x -= BLOCK_SIZE
                    if x <= left:
                        direction = 3
                        bottom -= BLOCK_SIZE
                        x = left

                elif direction == 3:  # up
                    pygame.draw.rect(
                        spiral_surface, (0, 0, 0),
                        (x, y, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    y -= BLOCK_SIZE
                    if y <= top:
                        direction = 0
                        left += BLOCK_SIZE
                        y = top

                if left >= right or top >= bottom:
                    finished = True
                    break

        screen.blit(spiral_surface, (0, 0))

        if finished:
            fade_alpha += 6
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.fill((255, 255, 255))
            fade.set_alpha(fade_alpha)
            screen.blit(fade, (0, 0))

            if fade_alpha >= 255:
                transition_complete = True

        pygame.display.flip()
    
    return True


# Run standalone if executed directly
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("transition")
    run_transition(screen)
    pygame.quit()
    sys.exit()
