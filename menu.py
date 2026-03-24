from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes

#Theme colors yAY!
MY_CUSTOM_THEME = pygame_menu.themes.THEME_DARK.copy()
MY_CUSTOM_THEME.title_close_button = False
TITLE_FONT = pygame_menu.font.FONT_BEBAS
FONT_COLOR = (215, 215, 0)
TITLE_BG_COLOR = (20, 20, 40)
BAR_STYLE = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE

# Widget styles
THEME_WIDGET_FONT = pygame_menu.font.FONT_COMIC_NEUE
WIDGET_FONT_COLOR = (200, 200, 200)
THEME_WIDGET_ALIGNMENT = pygame_menu.locals.ALIGN_CENTER

RESOLUTIONS = [
    ("640 x 480",   (640,  480)),
    ("800 x 600",   (800,  600)),
    ("1280 x 720",  (1280, 720)),
    ("1920 x 1080", (1920, 1080)),
]

def apply_resolution(surface_ref, menu_ref, value):
    new_w, new_h = value
    new_surface = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
    surface_ref[0] = new_surface
    for menu in menu_ref:
        if menu is not None:  # ← guard: skip if menu isn't built yet
            menu.resize(new_w, new_h)

def options_menu(surface_ref, main_menu_obj_ref):
    opts = pygame_menu.Menu(
        title="Options",
        width=surface_ref[0].get_width(),
        height=surface_ref[0].get_height(),
        theme=MY_CUSTOM_THEME,
    )

    opts.add.selector(
        title="Resolution: ",
        items=RESOLUTIONS,
        default=0,
        onchange=lambda selected, value: apply_resolution(
            surface_ref,
            [opts, main_menu_obj_ref[0]],
            value,  # pass value directly — it's already (w, h)
        ),
    )

    opts.add.vertical_margin(20)
    opts.add.button("Back", pygame_menu.events.BACK)
    return opts

def main_menu(surface_ref, start_callback):
    main_menu_obj_ref = [None]
    opts = options_menu(surface_ref, main_menu_obj_ref)

    La_carte = pygame_menu.Menu(
        title="Wood Hollow Academy",
        width=surface_ref[0].get_width(),
        height=surface_ref[0].get_height(),
        theme=MY_CUSTOM_THEME,
    )

    main_menu_obj_ref[0] = La_carte

    La_carte.add.label("SUP DUDE", font_size=30)
    La_carte.add.vertical_margin(20)
    La_carte.add.button("Start Game", start_callback)
    La_carte.add.button("Options", opts)
    La_carte.add.button("QUIT", pygame_menu.events.EXIT)

    return La_carte

# ── minimal main loop ────────────────────────────────────────────────────────
if __name__ == "__main__":
    pygame.init()
    surface_ref = [pygame.display.set_mode((640, 480), pygame.RESIZABLE)]
    pygame.display.set_caption("Wood Hollow Academy")

    menu = main_menu(surface_ref, lambda: print("Game started!"))

    clock = pygame.time.Clock()
    while True:
        surface_ref[0].fill(BG_COLOR)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface_ref[0])

        pygame.display.flip()
        clock.tick(60)