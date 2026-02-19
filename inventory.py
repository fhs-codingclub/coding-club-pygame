import pygame
import random

# --- Setup ---
pygame.init()

# --- Customizable Settings ---
WIDTH = 600         # Window width
HEIGHT = (WIDTH*(3/4))        # Window height
BG_COLOR = (255, 255, 255)     # Background color
GRID_SIZE = round(WIDTH/20) # Size of the grid, by default will be 1/20th of width
UI_SCALE = (WIDTH/400) # Scaling for UI elements

PLAYER_COLOR = (50, 100, 200)  # Player color
PLAYER_SIZE = GRID_SIZE     # Player size
pygame.key.set_repeat(100)
PLAYER_SPEED = 2

TARGET_COLOR = (200, 50, 50)   # Target color
TARGET_SIZE = GRID_SIZE       # Target size
moving = False
direction = 1


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Get the Red Square!")

GRAY = (100,100,100)
WHITE = (255,255,255)

# --- Player initial position ---
# Center the player in the window
player_x_grid = 0
player_y_grid = 0


# --- Target initial position ---
target_x_grid = 5
target_y_grid = 5



player_x = player_x_grid * GRID_SIZE
player_y = player_y_grid * GRID_SIZE
target_x = target_x_grid * GRID_SIZE
target_y = target_y_grid * GRID_SIZE
collide_rect = (0,0,0,0)
# --- Font for win message ---
font = pygame.font.Font(None, 60) # Use default font, size 60
font2 = pygame.font.Font(None, 15*(round(UI_SCALE)))
font3 = pygame.font.Font(None, 8*(round(UI_SCALE)))
font4 = pygame.font.Font(None, 12*(round(UI_SCALE)))
# --- Clock for controlling frame rate ---
clock = pygame.time.Clock()
# --- Inventory ---
# Item properties: ["Title", "Description", "Type", Value, Image]
# Air is effectively an empty space
attack = 0
defense = 0
health = 1
maxhealth = 10
item1 = ["sword", "A sharp sword", "weapon", 1, (pygame.image.load("rocketship.gif"))]
item2 = ["helmet", "A helmet", "armor", 1, (pygame.image.load("download (1).png"))]
item3 = ["apple", "An apple", "healing", 1, (pygame.image.load("apple.png"))]
inventory = [item1, 'air', item2, item3, 'air', 'air', 'air', 'air']
armor = 'air'
weapon = 'air'
inv_space_1 = pygame.Rect((115*UI_SCALE),(95*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_2 = pygame.Rect((160*UI_SCALE),(95*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_3 = pygame.Rect((205*UI_SCALE),(95*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_4 = pygame.Rect((250*UI_SCALE),(95*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_5 = pygame.Rect((115*UI_SCALE),(160*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_6 = pygame.Rect((160*UI_SCALE),(160*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_7 = pygame.Rect((205*UI_SCALE),(160*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inv_space_8 = pygame.Rect((250*UI_SCALE),(160*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
inventory_selected = 10 # A value of 10 means no item
inventory_hover = 10
inventory_list = [inv_space_1,inv_space_2,inv_space_3,inv_space_4,inv_space_5,inv_space_6,inv_space_7,inv_space_8]
armor_space = pygame.Rect((60*UI_SCALE),(95*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
weapon_space = pygame.Rect((60*UI_SCALE),(160*UI_SCALE),(35*UI_SCALE),(45*UI_SCALE))
# --- Game State ---
game_won = False
state = "normal"

# Define functions
def additem(item):
  i = 0
  while i <= 7:
    if inventory[i] == "air":
      free_space = i
      i = 20
    else:
      free_space = 10
    i += 1
  if free_space == 10:
    return(False)
  else:
    inventory[free_space] = item
    return(True)

# --- Game Loop ---
running = True
while running:
    # --- Control Frame Rate ---
    # This ensures the loop runs at a maximum of 60 frames per second
    clock.tick(60)
    # --- Event loop ---
    # Check for events like closing the window
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
               
               
               
    # Grid-based movement
      if event.type == pygame.KEYDOWN:
        if not game_won and not moving:
          if event.key == pygame.K_LEFT and player_x_grid > 0 and state == "normal":
            moving = True
            direction = "left"
          if event.key == pygame.K_RIGHT and player_x_grid < ((WIDTH/GRID_SIZE)-1) and state == "normal":
            moving = True
            direction = "right"
          if event.key == pygame.K_UP and player_y_grid > 0 and state == "normal":
            moving = True
            direction = "up"
          if event.key == pygame.K_DOWN and player_y_grid < ((HEIGHT/GRID_SIZE)-1) and state == "normal":
            moving = True
            direction = "down"
            
            
          if event.key == pygame.K_e:
            if state == "normal":
              state = "inventory"
            else:
              state = "normal"
      if event.type == pygame.MOUSEBUTTONDOWN and state == "inventory" and not inventory_hover == 10:
        if inventory_hover == 20: # This checks if the "Use" button is being hovered over
          if inventory[inventory_selected] == "air":
            1 == 1 # Do nothing if air is selected
          else:
            temporary = inventory[inventory_selected]
            if temporary[2] == "weapon":
              temporary2 = weapon
              weapon = inventory[inventory_selected]
              inventory[inventory_selected] = temporary2
              attack = temporary[3]
              inventory_selected = 10
            elif temporary[2] == "armor":
              temporary2 = armor
              armor = inventory[inventory_selected]
              inventory[inventory_selected] = temporary2
              defense = temporary[3]
              inventory_selected = 10
            else:
              inventory[inventory_selected] = "air"
              health += temporary[3]
              if health > maxhealth:
                health = maxhealth
              inventory_selected = 10
        elif inventory_hover == 21: # This checks if the armor slot is being hovered over
          if armor == "air": # If no armor is used, do nothing
            1 == 1
          else:
            success = additem(armor)
            if success:
              armor = "air"
              defense = 0
            else:
              1 == 1
                
        elif inventory_hover == 22: # This checks if the weapon slot is being hovered over
          if weapon == "air":
            1 == 1
          else:
            success = additem(weapon)
            if success:
              weapon = "air"
              attack = 0
            else:
               1 == 1
        else:
          if inventory_selected == inventory_hover:
            inventory_selected = 10
          else:
            if inventory_selected == 10:
              inventory_selected = inventory_hover
            else:
              temporary = inventory[inventory_selected]
              inventory[inventory_selected] = inventory[inventory_hover]
              inventory[inventory_hover] = temporary
              inventory_selected = 10
            
              
              
      
    # --- Player Movement (only if the game is not won yet) ---


    # --- Border Check ---
    if player_x_grid < 0.5:
      player_x_grid = 0
    if player_x_grid >= (WIDTH/GRID_SIZE):
      player_x_grid = ((WIDTH/GRID_SIZE)-1)
    if player_y_grid < 0.5:
      player_y_grid = 0
    if player_y_grid >= (HEIGHT/GRID_SIZE):
      player_y_grid = ((HEIGHT/GRID_SIZE)-1)
    mouse_pos = pygame.mouse.get_pos()
    i = 0
    while i <= 7:
      colliding = inventory_list[i].collidepoint(mouse_pos)
      if colliding == True:
        collide_rect = inventory_list[i]
        inventory_hover = i
        i = 20
      else:
        collide_rect = (0,0,0,0)
        inventory_hover = 10
      i += 1
    if pygame.Rect((245*UI_SCALE),(255*UI_SCALE),(35*UI_SCALE),(20*UI_SCALE)).collidepoint(mouse_pos):
      inventory_hover = 20
    if armor_space.collidepoint(mouse_pos):
      inventory_hover = 21
    if weapon_space.collidepoint(mouse_pos):
      inventory_hover = 22
     
          
    keys = pygame.key.get_pressed()

          
    if not moving:
      player_x = player_x_grid * GRID_SIZE
      player_y = player_y_grid * GRID_SIZE
      target_x = target_x_grid * GRID_SIZE
      target_y = target_y_grid * GRID_SIZE
      if keys[pygame.K_LSHIFT]:
        PLAYER_SPEED = (GRID_SIZE/5)
      else:
        PLAYER_SPEED = (GRID_SIZE/10)
    if moving:
      if direction == "up": 
        player_y -= PLAYER_SPEED
        if player_y % GRID_SIZE == 0:
          moving = False
          player_y_grid -= 1
      if direction == "down": 
        player_y += PLAYER_SPEED
        if player_y % GRID_SIZE == 0:
          moving = False
          player_y_grid += 1
      if direction == "left": 
        player_x -= PLAYER_SPEED
        if player_x % GRID_SIZE == 0:
          moving = False
          player_x_grid -= 1
      if direction == "right": 
        player_x += PLAYER_SPEED
        if player_x % GRID_SIZE == 0:
          moving = False
          player_x_grid += 1

    # --- Create Rects for Collision ---
    # We create these fresh each loop to have the latest coordinates
    player_rect = pygame.Rect((player_x), (player_y), PLAYER_SIZE, PLAYER_SIZE)
    target_rect = pygame.Rect((target_x), (target_y), TARGET_SIZE, TARGET_SIZE)

    # --- Collision Check ---
    if player_rect.colliderect(target_rect):
      additem(item3)
      target_x_grid = random.randint(0,19)
      target_y_grid = random.randint(0,14)
      target_x = target_x_grid * GRID_SIZE
      target_y = target_y_grid * GRID_SIZE

    # --- Drawing ---
    screen.fill(BG_COLOR)
     
    # Draw the target
    pygame.draw.rect(screen, TARGET_COLOR, target_rect)
     
    # Draw the player
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
     

    # Draw the inventory
    if state == "inventory":
      # Draw stats screen
      pygame.draw.rect(screen, GRAY, ((310*UI_SCALE),(50*UI_SCALE),(90*UI_SCALE),(200*UI_SCALE)))
      # Draw attack
      stats_text1 = font4.render(("Attack: " + str(attack)), True, (0,0,0))
      screen.blit(stats_text1,((320*UI_SCALE),(60*UI_SCALE)))
      # Draw defense
      stats_text2 = font4.render(("Defense: " + str(defense)), True, (0,0,0))
      screen.blit(stats_text2,((320*UI_SCALE),(85*UI_SCALE)))
      # Draw health
      stats_text3 = font4.render(("Health: " + str(health) + "/" + str(maxhealth)), True, (0,0,0))
      screen.blit(stats_text3,((320*UI_SCALE),(110*UI_SCALE)))
      
      pygame.draw.rect(screen, GRAY, ((50*UI_SCALE),(75*UI_SCALE),(250*UI_SCALE),(150*UI_SCALE)))
      pygame.draw.rect(screen, GRAY, ((100*UI_SCALE),(250*UI_SCALE),(200*UI_SCALE),(50*UI_SCALE)))
      i = 0
      while i <= 7:
        if inventory[i] == "air":
          pygame.draw.rect(screen, WHITE, inventory_list[i])
          if i == inventory_selected:
            pygame.draw.rect(screen, (200,200,200), inventory_list[inventory_selected])  
        else:
          pygame.draw.rect(screen, WHITE, inventory_list[i])
          if i == inventory_selected:
            pygame.draw.rect(screen, (200,200,200), inventory_list[inventory_selected])
          rect_topleft = inventory_list[i].topleft
          screen.blit(pygame.transform.scale(inventory[i][4],((35*UI_SCALE),(45*UI_SCALE))), rect_topleft)
        i += 1
      if armor == "air":
        pygame.draw.rect(screen, WHITE, armor_space)
      else:
        pygame.draw.rect(screen, WHITE, armor_space)
        rect_topleft = armor_space.topleft
        screen.blit(pygame.transform.scale(armor[4],((35*UI_SCALE),(45*UI_SCALE))), rect_topleft)
      if weapon == "air":
        pygame.draw.rect(screen, WHITE, weapon_space)
      else:
        pygame.draw.rect(screen, WHITE, weapon_space)
        rect_topleft = weapon_space.topleft
        screen.blit(pygame.transform.scale(weapon[4],((35*UI_SCALE),(45*UI_SCALE))), rect_topleft)
      if not inventory_selected == 10:
        if inventory[inventory_selected] == "air":
          description_text = font3.render("Literally nothing", True, (0,0,0))
          screen.blit(description_text, ((110*UI_SCALE),(260*UI_SCALE)))
        else:
          current_item = inventory[inventory_selected]
          title_text = font2.render(current_item[0], True, (0,0,0))
          description_text = font3.render(current_item[1], True, (0,0,0))
          screen.blit(description_text, ((110*UI_SCALE),(275*UI_SCALE)))
          screen.blit(title_text, ((110*UI_SCALE),(260*UI_SCALE)))
          pygame.draw.rect(screen, (200,200,200), ((245*UI_SCALE),(255*UI_SCALE),(35*UI_SCALE),(20*UI_SCALE)))
          use_text = font2.render("Use", True, (0,0,0))
          screen.blit(use_text, ((250*UI_SCALE),(260*UI_SCALE)))
          
    # --- Show Win Message if Game is Won ---
    if game_won:
      win_text = font.render("You Win!", True, (0, 150, 0))
      # Center the text
      text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
      screen.blit(win_text, text_rect)

    # --- Update Display ---
    pygame.display.update()

# --- Quit Pygame ---
pygame.quit()
