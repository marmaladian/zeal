import pygame as pg
import numpy as np

class UITile:
    size = (8, 8)    # pixel size of tiles

    def __init__(self, name: str, surface : pg.Surface = None) -> None:
        if surface is None:
            self.surface = pg.Surface(UITile.size)
        else:
            self.surface = surface

    def set_image(self, surface : pg.Surface):
        self.surface = surface

    def draw(self, canvas : pg.Surface, position):
        canvas.blit(self.surface, (position[0] * self.size[0], position[1] * self.size[1]))