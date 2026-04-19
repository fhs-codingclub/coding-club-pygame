import pygame
import sys
import random
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle
from menu import main_menu
from overworld import run_overworld
from player import Player 
from inventory import InventorySystem

def start_battle(screen, player, inventory_sys, enemy_name):
    pygame.mixer.music.fadeout(1000)  
    pygame.mixer.music.load("py/assets/moosic/copyrightedplaceholdermusic.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)  
    vol = pygame.mixer.music.get_volume()
    print("moosic volume for battle is", vol)
    
    # If transition completed, start the battle
    if run_transition(screen):
        result, updated_player = run_battle(screen, player, inventory_sys, enemy_name)
        
         # After battle, restore/continue overworld music
        pygame.mixer.music.fadeout(500)
        try:
            pygame.mixer.music.load("py/assets/moosic/Exploration_song_no_drums.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.2)
            vol = pygame.mixer.music.get_volume()
            print("overworld Volume is set to:", vol)
        except Exception:
            pass
        return result, updated_player
    else:
        # Transition was quit
        return "QUIT"

def play(screen):
    pygame.display.set_caption("Adventure Time!")
    pygame.mixer.music.fadeout(1000) 

    pygame.mixer.music.load("py/assets/moosic/Exploration_song_no_drums.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    vol = pygame.mixer.music.get_volume()
    print("overworld Volume is set to:", vol)

    player_state = Player(2, 2)
    inventory = InventorySystem(WIDTH, HEIGHT)
    boss1defeated = False

    while True:
        result, inventory, player_state = run_overworld(screen, inventory, player_state, boss1defeated)

        if result == "QUIT":
            return
        
        elif result == "WIN_GAME":
            print("YOU ESCAPED!")
            return
        
        elif result in ("START_BATTLE", "RANDOM_BATTLE"):
            
            # Keep state of player fix for bug
            saved_inventory = inventory
            enemy_to_fight = player_state.last_enemy_name
            battle_result, player_state = start_battle(screen, player_state, inventory, enemy_to_fight)
            pygame.display.set_caption("Adventure Time!")
            
            if battle_result == "WIN":
                boss1defeated = True
            if battle_result == "QUIT":
                return
            if player_state.hp <= 0:
                print("Game Over!")
                return

def main():
    
    # Initialize
    pygame.init()
    pygame.display.set_caption("Wood Hollow Academy")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.init()
    
    # Load music
    pygame.mixer.music.load("py/assets/moosic/Main-Menu-Theme.mp3")
    pygame.mixer.music.play(-1)
    vol = pygame.mixer.music.get_volume()
    print("moosic volume for menu is", vol)

    # Run the main menu first
    surface_ref = [screen]
    my_menu = main_menu(surface_ref, lambda: play(surface_ref[0]))
    
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