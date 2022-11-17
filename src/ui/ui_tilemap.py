from __future__ import annotations
import random
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.ui_manager import *
    
import pygame as pg
import numpy as np

from ui.ui_tile import *

from world import Map

class UITileMap:

    def __init__(self, ui: UIManager):
        self.ui = ui
        self.size = ui.map_size

        w, h = self.size
        th, tw = self.ui.tile_size
        self.surface = pg.Surface((tw*w, th*h))

    def render(self, map: Map, z: int):
        # DRAW TERRAIN FIRST
        terrain_data = map.layers[z].terrain
        m, n = terrain_data.shape
        th, tw = self.ui.tile_size
        for i in range(m):
            for j in range(n):
                # NEED TO GET SPRITE FOR BLOCK
                # MAP HOLDS BLOCK NAME
                blk = map.tile_at((i, j, z))
                tile = self.ui.get_tile(blk.tile)
                #tile : UITile = self.ui.get_tile(terrain_data[i, j])
                tile.draw(self.surface, blk.colours, (i*tw, j*th))
                # self.surface.blit(tile.surface, (i*tw, j*th))
        
        # DRAW ITEMS NEXT
        for pos, items in map.layers[z].items.items():
            # find highest priority item
            # get that item's image
            self.ui.get_tile('chest').draw(self.surface, (3, 1), (pos[0] * 8, pos[1] * 8))

        # DRAW ACTORS
        for actor in map.actors:
            if actor.position[2] == z:
                tile = self.ui.get_tile(actor.tile_id)
                tile.draw(self.surface, (0, 4), (actor.position[0] * tw, actor.position[1] * th))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        # print(self.map)
        # print(self.map.shape)
        # self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        # print(self.map)
        # self.render()

    def tile_at(self, position: tuple[int, int]):
        x, y = position
        if (0 <= x < self.size[0]) and (0 <= y < self.size[1]):
            return self.tileset.tiles[self.map[x, y]]    
        else:
            return self.border_tile

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'