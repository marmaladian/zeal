import pygame as pg
import numpy as np

class Tile:
    size = (8, 8)    # pixel size of tiles

    def __init__(self, surface : pg.Surface, walkable : bool) -> None:
        self.surface = surface #pg.Surface(Tile.size)
        self.walkable = walkable

    def set_image(self, surf : pg.Surface):
        self.surface = surf

    def draw(self, canvas : pg.Surface, position):
        canvas.blit(self.surface, (position[0] * self.size[0], position[1] * self.size[1]))