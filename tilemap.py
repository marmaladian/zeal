import pygame as pg
import numpy as np

class TileMap:

    def __init__(self, tileset, border_tile, size = (32, 20), rect = None):
        self.tileset = tileset
        self.border_tile = border_tile
        self.size = size
        self.map = np.zeros(size, dtype=int)

        w, h = self.size
        th, tw = tileset.tile_size
        self.surface = pg.Surface((tw*w, th*h))
        if rect:
            self.rect = pg.Rect(rect)
        else:
            self.rect = self.surface.get_rect()

    def render(self):
        m, n = self.map.shape
        th, tw = self.tileset.tile_size
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.surface.blit(tile.surface, (i*tw, j*th))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        print(self.map)
        print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def tile_at(self, position: tuple[int, int]):
        x, y = position
        if (0 <= x < self.size[0]) and (0 <= y < self.size[1]):
            return self.tileset.tiles[self.map[x, y]]    
        else:
            return self.border_tile

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'