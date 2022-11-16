import pygame as pg
import numpy as np
from ui.ui_palette import palette

class UITile:

    def __init__(self, name: str, size: tuple[int, int], data: int) -> None:
        self.size = size
        self.bits = self.size[0] * self.size[1]
        self.data = data
        self.colorways = {}

    def create_surface(self, colors: tuple[int, int]) -> pg.Surface:
        surf = pg.Surface(self.size)
        fg, bg = colors
        surf.fill(palette[bg])
        for bit_offset in range(self.bits):
            if self.data & (1 << bit_offset):   # mask to test bit
                y = bit_offset // self.size[0]
                x = bit_offset % self.size[0]
                surf.set_at((x, y), palette[fg])
        self.colorways[colors] = surf
        return surf

    def draw(self, canvas : pg.Surface, colors: tuple[int, int], position, frame: int = None):
        if colors in self.colorways:
            surf = self.colorways[colors]
        else:
            surf = self.create_surface(colors)
        
        canvas.blit(surf, position)

class UIAnimTile(UITile):

    def __init__(self, name: str, surface: pg.Surface = None) -> None:
        super().__init__(name, surface)

    def draw(self, surf: pg.Surface, position, palette: tuple[int, int], frame: int):
        pass
        
