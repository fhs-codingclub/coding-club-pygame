import pygame
import sys
import random
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle
from menu import main_menu
from overworld import run_overworld

def start_battle(screen):
    pygame.mixer.music.fadeout(1000)  
    pygame.mixer.music.load("assets/moosic/copyrightedplaceholdermusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)  
    vol = pygame.mixer.music.get_volume()
    print("moosic volume for battle is", vol)
    
    # If transition completed, start the battle
    if run_transition(screen):
        result = run_battle(screen)
        
         # After battle, restore/continue overworld music
        pygame.mixer.music.fadeout(500)
        try:
            pygame.mixer.music.load("assets/moosic/Exploration_song_no_drums.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
            vol = pygame.mixer.music.get_volume()
            print("overworld Volume is set to:", vol)
        except Exception:
            pass
        return result
    else:
        # Transition was quit
        return "QUIT"

def play(screen):
    pygame.display.set_caption("Adventure Time!")
    pygame.mixer.music.fadeout(1000) 

    pygame.mixer.music.load("assets/moosic/Exploration_song_no_drums.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    vol = pygame.mixer.music.get_volume()
    print("overworld Volume is set to:", vol)
    
    inventory = None
    player_state = None

    while True:
        result, inventory, player_state = run_overworld(screen, inventory, player_state)

        if result == "QUIT":
            return
        elif result in ("START_BATTLE", "RANDOM_BATTLE"):
            
            # Keep state of player fix for bug
            saved_state = dict(player_state) if player_state else None
            saved_inventory = inventory

            battle_result = start_battle(screen)
            pygame.display.set_caption("Adventure Time!")

            # Restore the players state 
            player_state = saved_state
            inventory = saved_inventory

            if battle_result == "QUIT":
                return

def main():
    
    # Initialize
    pygame.init()
    pygame.display.set_caption("Wood Hollow Academy")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.init()
    
    # Load music
    pygame.mixer.music.load("assets/moosic/Main-Menu-Theme.mp3")
    pygame.mixer.music.play(-1)
    vol = pygame.mixer.music.get_volume()
    print("moosic volume for menu is", vol)

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