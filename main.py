import pygame
import sys
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle
from menu import main_menu

start = True


def play():
    pygame.display.set_caption("DEBUG!!!")
    # Run the transition/loader second MWAHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAAHAHAHAhAHAHAHAhAHAHAHAHAHAhAHAHAHAhAHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHAHAHA Help me
    if run_transition(screen):
        # If transition completed (didn't quit), start the battle
        run_battle(screen)
        
def main():
    pygame.init()
    pygame.display.set_caption("DEBUG!!!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    

    #Run the main menu first
    if start:
        my_menu = main_menu(screen, play)
        
        run_menu = True
        while my_menu.is_enabled():
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit
            if my_menu.is_enabled():
                my_menu.update(events)
                my_menu.draw(screen)
                pygame.display.update()
            else:
                run_menu = False
    play()


if __name__ == "__main__":
    main()
