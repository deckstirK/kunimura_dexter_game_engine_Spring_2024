import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.rect = pg.Rect(0, 0, self.tilewidth * TILESIZE, self.tileheight * TILESIZE)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pg.rect.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    # def apply(self, sprite):
    #     # Adjust the sprite's position based on the camera's position
    #     new_x = sprite.rect.x - self.x
    #     new_y = sprite.rect.y - self.y
    #     return pg.rect.Rect(new_x, new_y, sprite.rect.width, sprite.rect.height)
    def apply(self, target):
        return target.rect.move(self.camera.topleft)
    
    def update(self, target):
        # Center the camera on the target
        x = -target.rect.x + int(self.width / 2)
        y = -target.rect.y + int(self.height / 2)
        self.camera.topleft = (x, y)

        # # Limit scrolling to the map size
        # x = min(0, x)  # Left
        # x = max(-(self.width - WIDTH), x)  # Right
        # y = min(0, y)  # Top
        # y = max(-(self.height - HEIGHT), y)  # Bottom

        # self.camera = pg.Rect(x, y, self.width, self.height)
        # self.camera.clamp_ip(target.game_map.rect)

        def update(self, target):
            # Center the camera on the target
            x = -target.rect.x + int(WIDTH / 2)
            y = -target.rect.y + int(HEIGHT / 2)
            
            # Limit scrolling to the map size
            x = min(0, x)  # Left
            x = max(-(self.width - WIDTH), x)  # Right
            y = min(0, y)  # Top
            y = max(-(self.height - HEIGHT), y)  # Bottom

            # Update the position of the camera
            self.camera.topleft = (x, y)
            self.camera.clamp_ip(target.game_map.rect)