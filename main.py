import pygame
import sys
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DEBUG!!!")
    
    # Run the transition/loader first
    if run_transition(screen):
        # If transition completed (didn't quit), start the battle
        run_battle(screen)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()