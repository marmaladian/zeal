from ui.ui_tilemap import UITileMap
import pygame as pg

class UIManager:

    def __init__(self, screen_buffer: pg.Surface, ui_size, tile_set, tile_size, map_size) -> None:
        self.screen = screen_buffer
        self.size = ui_size
        self.tile_set = tile_set
        self.tile_size = tile_size
        self.map_size = map_size
        self.map = UITileMap(self)
        self.active_ui = None
        self.surface = pg.Surface((self.size[0] * self.tile_size[0], self.size[1] * self.tile_size[1]))

    def render(self, block_map, z_layer):
        # update
        self.map.render(block_map, z_layer)
        
        self.surface.blit(self.map.surface, self.tile_size)
        if self.active_ui:
            self.active_ui.render()
            self.surface.blit(self.active_ui.surface, (0, 0))

    def get_tile(self, index):
        return self.tile_set[index]