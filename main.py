import pygame
import sys
import random
from loader import run_transition, WIDTH, HEIGHT
from combat import run_battle
from menu import main_menu
from overworld import run_overworld
from player import Player 
from inventory import InventorySystem

<<<<<<< HEAD
persistent_player = Player(2, 2)
persistent_inventory = InventorySystem(WIDTH, HEIGHT)

def start_battle(screen, player, inventory_sys, enemy_name):
    pygame.mixer.music.fadeout(1000)  
    pygame.mixer.music.load("py/assets/moosic/copyrightedplaceholdermusic.mp3")
=======

def start_battle(real_screen):
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.load("assets/moosic/copyrightedplaceholdermusic.mp3")
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    vol = pygame.mixer.music.get_volume()
    print("moosic volume for battle is", vol)
<<<<<<< HEAD
    
    # If transition completed, start the battle
    if run_transition(screen):
        result, updated_player = run_battle(screen, player, inventory_sys, enemy_name)
        
         # After battle, restore/continue overworld music
=======

    if run_transition(real_screen):
        result = run_battle(real_screen)

>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
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
        return "QUIT"

<<<<<<< HEAD
def play(screen, player_state, inventory):
    pygame.display.set_caption("Wood Hollow Academy")
    pygame.mixer.music.fadeout(1000) 

    pygame.mixer.music.load("py/assets/moosic/Exploration_song_no_drums.mp3")
=======

def play(real_screen):
    pygame.display.set_caption("Adventure Time!")
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.load("assets/moosic/Exploration_song_no_drums.mp3")
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    vol = pygame.mixer.music.get_volume()
    print("overworld Volume is set to:", vol)

<<<<<<< HEAD
    boss1defeated = False

    while True:
        result, inventory, player_state = run_overworld(screen, inventory, player_state, boss1defeated)

        if result == "MENU":
            return # This exits the play() function and goes back to the menu loop

        elif result == "QUIT":
=======
    inventory = None
    player_state = None

    while True:
        result, inventory, player_state = run_overworld(real_screen, inventory, player_state)
        if result == "QUIT":
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
            return
        
        elif result == "WIN_GAME":
            print("YOU ESCAPED!")
            return
        
        elif result in ("START_BATTLE", "RANDOM_BATTLE"):
<<<<<<< HEAD
            
            # Keep state of player fix for bug
            saved_inventory = inventory
            enemy_to_fight = player_state.last_enemy_name
            battle_result, player_state = start_battle(screen, player_state, inventory, enemy_to_fight)
            pygame.display.set_caption("Adventure Time!")
            
            if battle_result == "WIN":
                boss1defeated = True
=======
            saved_state = dict(player_state) if player_state else None
            saved_inventory = inventory
            battle_result = start_battle(real_screen)
            pygame.display.set_caption("Adventure Time!")
            player_state = saved_state
            inventory = saved_inventory
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
            if battle_result == "QUIT":
                return
            if player_state.hp <= 0:
                print("Game Over!")
                return


def main():
    pygame.init()
    pygame.display.set_caption("Wood Hollow Academy")
    pygame.mixer.init()
<<<<<<< HEAD
    
    # Load music
    pygame.mixer.music.load("py/assets/moosic/Main-Menu-Theme.mp3")
=======

    # Start at 800x600, resizable — game content always renders at 640x480 inside
    surface_ref = [pygame.display.set_mode((800, 600), pygame.RESIZABLE)]

    pygame.mixer.music.load("assets/moosic/Main-Menu-Theme.mp3")
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
    pygame.mixer.music.play(-1)
    vol = pygame.mixer.music.get_volume()
    print("moosic volume for menu is", vol)

<<<<<<< HEAD
    # Run the main menu first
    surface_ref = [screen]
    my_menu = main_menu(surface_ref, lambda: play(surface_ref[0], persistent_player, persistent_inventory))
    
    # Menu loop
=======
    my_menu = main_menu(surface_ref, lambda: play(surface_ref[0]))

    clock = pygame.time.Clock()
>>>>>>> db0ac6f (adapt resolutions to scale "properly", have the gayme in the middle and black bars)
    while my_menu.is_enabled():
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Menu draws directly to the window — pygame_menu handles its own sizing
        surface_ref[0].fill((0, 0, 0))
        my_menu.update(events)
        my_menu.draw(surface_ref[0])
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()