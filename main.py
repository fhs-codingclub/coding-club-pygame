import pygame
import sys
import random
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle
from menu import main_menu
from overworld import run_overworld

def start_battle(screen):
    """Handles the transition and battle sequence"""
    pygame.mixer.music.fadeout(1000)  

    # If transition completed (didn't quit), start the battle
    if run_transition(screen):
        run_battle(screen)

def play(screen):
    """Main game loop - runs the overworld"""
    pygame.display.set_caption("Adventure Time!")
    pygame.mixer.music.fadeout(1000) 

    # Optional: Change music for overworld
    # pygame.mixer.music.load("assets/Overworld-Theme.mp3")
    # pygame.mixer.music.play(-1)
    
    while True:
        result = run_overworld(screen)
        
        if result == "QUIT":
            return
        elif result == "START_BATTLE":
            start_battle(screen)
            pygame.display.set_caption("Adventure Time!")
        elif result == "RANDOM_BATTLE":
            start_battle(screen)
            pygame.display.set_caption("Adventure Time!")

def main():
    # Initialize
    pygame.init()
    pygame.display.set_caption("DEBUG!!!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.init()
    
    # Load music
    pygame.mixer.music.load("assets/Main-Menu-Theme.mp3")
    pygame.mixer.music.play(-1)
    
    # Run the main menu first
    my_menu = main_menu(screen, lambda: play(screen))
    
    # Menu loop
    while True:
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
            # Menu was closed, exit the game
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()