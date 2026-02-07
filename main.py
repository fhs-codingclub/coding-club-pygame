import pygame
import sys
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle
from menu import main_menu


start = True


def play(screen):
    pygame.display.set_caption("DEBUG!!!")
    pygame.mixer.music.fadeout(1000)  

    #If transition completed (didn't quit), start the battle
    if run_transition(screen):
       run_battle(screen)
        
def main():
    #Initialize
    pygame.init()
    pygame.display.set_caption("DEBUG!!!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.init()

    # Load music
    pygame.mixer.music.load("assets/Main-Menu-Theme.mp3")
    pygame.mixer.music.play(-1)

    #Run the main menu first
    if start:
        my_menu = main_menu(screen, lambda: play(screen))
        
        run_menu = True
        while my_menu.is_enabled():
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if my_menu.is_enabled():
                my_menu.update(events)
                my_menu.draw(screen)
                pygame.display.update()
            else:
                run_menu = False
    
    #Start the battle after the play is clicked
    play(screen)


if __name__ == "__main__":
    main()
