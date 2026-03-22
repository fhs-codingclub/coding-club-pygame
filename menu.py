from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes

#Theme colors yAY!
MY_CUSTOM_THEME = pygame_menu.themes.THEME_DARK.copy()
BG_COLOR = (30, 30, 60)
TITLE_FONT = pygame_menu.font.FONT_BEBAS
FONT_COLOR = (215, 215, 0)
TITLE_BG_COLOR = (20, 20, 40)
BAR_STYLE = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE

#Widget styles bleh
THEME_WIDGET_FONT = pygame_menu.font.FONT_COMIC_NEUE
WIDGET_FONT_COLOR = (200, 200, 200)
THEME_WIDGET_ALIGNMENT = pygame_menu.locals.ALIGN_CENTER

def main_menu(surface, start_callback):
	#Start callback function that runs when "Play" is clicked
	La_carte = pygame_menu.Menu(
	title="Wood Hollow Academy",
	width=surface.get_width(),
	height=surface.get_height(),
	theme=MY_CUSTOM_THEME
	)
	
	#UI ELEMENTS
	La_carte.add.label("SUP DUDE", font_size=30)
	La_carte.add.vertical_margin(20)
	La_carte.add.button("Start Game", start_callback)
	La_carte.add.button("Options", lambda: print("Options Menu Open"))
	La_carte.add.button("QUIT", pygame_menu.events.EXIT)
	
	return La_carte
