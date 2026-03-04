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
    pygame.mixer.music.load("assets/copyrightedplaceholdermusic.mp3")
    pygame.mixer.music.play(-1)
    # If transition completed (didn't quit), start the battle
    if run_transition(screen):
        result = run_battle(screen)
        # After battle, restore/continue overworld music
        pygame.mixer.music.fadeout(500)
        try:
            pygame.mixer.music.load("assets/Exploration_song_no_drums.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass
        return result
    else:
        # Transition was quit
        return "QUIT"

def play(screen):
    """Main game loop - runs the overworld"""
    pygame.display.set_caption("Adventure Time!")
    pygame.mixer.music.fadeout(1000) 

    # Optional: Change music for overworld
    pygame.mixer.music.load("assets/Exploration_song_no_drums.mp3")
    pygame.mixer.music.play(-1)
    
    inventory = None  # Will be created on first run_overworld call
    
    while True:
        result, inventory = run_overworld(screen, inventory)
        
        if result == "QUIT":
            return
        elif result == "START_BATTLE":
            battle_result = start_battle(screen)
            pygame.display.set_caption("Adventure Time!")
            if battle_result == "QUIT":
                return
        elif result == "RANDOM_BATTLE":
            battle_result = start_battle(screen)
            pygame.display.set_caption("Adventure Time!")
            if battle_result == "QUIT":
                return

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
    while my_menu.is_enabled():
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        my_menu.update(events)
        my_menu.draw(screen)
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()