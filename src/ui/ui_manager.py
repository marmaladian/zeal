from ui.ui_tilemap import UITileMap
import pygame as pg

class UIManager:

    def __init__(self, ui_size, tile_set, tile_size, map_size) -> None:
        self.size = ui_size
        self.tile_set = tile_set
        self.tile_size = tile_size
        self.map_size = map_size
        self.map = UITileMap(self)
        self.surface = pg.Surface((self.size[0] * self.tile_size[0], self.size[1] * self.tile_size[1]))

    def render(self, block_map, z_layer):
        self.map.render(block_map, z_layer)
        self.surface.blit(self.map.surface, self.tile_size)

    def get_tile(self, index):
        return self.tile_set[index]