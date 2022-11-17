from ui.ui_tilemap import UITileMap
from ui.ui_text import UIText
import pygame as pg

class UIManager:

    def __init__(self, screen_buffer: pg.Surface, ui_config: dict, tile_set) -> None:
        self.ui_config = ui_config
        self.screen = screen_buffer
        self.size = ui_config['screen_size']
        self.tile_set = tile_set
        self.tile_size = ui_config['tile_size']
        self.map_size = ui_config['map_size']
        self.map = UITileMap(self) # abstract these into a UI elements list?
        self.active_ui = None # instead of tracking ui_mode in the main loop, check whether active_ui is the game map?
        self.surface = pg.Surface((self.size[0] * self.tile_size[0], self.size[1] * self.tile_size[1]))
        self.text_normal = UIText(pg.image.load('img/text_atlas.png'), (8, 8))
        self.text_invert = UIText(pg.image.load('img/text_atlas_inv.png'), (8, 8))

    def render(self, block_map, z_layer):
        # update
        self.map.render(block_map, z_layer)
        
        self.surface.fill(pg.Color(12, 16, 28))
        self.surface.blit(self.map.surface, self.to_pixel_pos(self.ui_config['map_position']))

        # render stats
        
        status_line = self.text_normal.create_surface('VIT 11  HEAT 30', 0)
        self.surface.blit(status_line, self.to_pixel_pos(self.ui_config['status_position']))

        if self.active_ui:
            self.active_ui.render()
            self.surface.blit(self.active_ui.surface, self.to_pixel_pos(self.ui_config['left_panel_position']))

    def get_tile(self, name):
        return self.tile_set[name]

    def to_pixel_pos(self, tile_pos: tuple[int, int]):
        return (tile_pos[0] * self.tile_size[0], tile_pos[1] * self.tile_size[1])

    def to_tile_pos(self, pixel_pos: tuple[int, int]):
        return (pixel_pos[0] // self.tile_size[0], pixel_pos[1] // self.tile_size[1])