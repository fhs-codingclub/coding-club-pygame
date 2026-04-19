import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        # 1. Load the map data
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        
        # 2. Extract collisions immediately upon loading
        self.collisions = []
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "collision":
                    for obj in layer:
                        # Store the Rects so the player can "hit" them
                        self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, 
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        # Create a surface and draw all the tiles onto it once
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface