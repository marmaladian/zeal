import pygame as pg
from src.block import Block

class TileSet:
    def __init__(self, tile_size = (8, 8)) -> None:
        self.tiles = []
        self.tile_size = tile_size

    def add(self, t : Block):
        self.tiles.append(t)

    def tile(self, index : int):
        return self.tiles[index]

# import pygame as pg

# class Tileset:
#     def __init__(self, file, size=(8, 8), margin = 0, spacing  = 0):
#         self.file = file
#         self.size = size
#         self.margin = margin
#         self.spacing = spacing
#         self.image = pg.image.load(file)
#         self.rect = self.image.get_rect()
#         self.tiles = []
#         self.load()


#     def load(self):
#         self.tiles = []
#         x0 = y0 = self.margin
#         w, h = self.rect.size
#         dx = self.size[0] + self.spacing
#         dy = self.size[1] + self.spacing
        
#         for x in range(x0, w, dx):
#             for y in range(y0, h, dy):
#                 tile = pg.Surface(self.size)
#                 tile.blit(self.image, (0, 0), (x, y, *self.size))
#                 self.tiles.append(tile)

#     def __str__(self):
#         return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'