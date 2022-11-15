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
        self.map = UITileMap(self)
        self.active_ui = None
        self.surface = pg.Surface((self.size[0] * self.tile_size[0], self.size[1] * self.tile_size[1]))
        self.text_normal = UIText(pg.image.load('img/text_atlas.png'), (8, 8))

    def render(self, block_map, z_layer):
        # update
        self.map.render(block_map, z_layer)
        
        self.surface.fill(pg.Color(12, 16, 28))
        self.surface.blit(self.map.surface, (self.ui_config['map_position'][0] * self.ui_config['tile_size'][0], self.ui_config['map_position'][1] * self.ui_config['tile_size'][1]))

        # render stats
        
        status_line = self.text_normal.create_surface('VIT 11  HEAT 33', 0)
        self.surface.blit(status_line, (self.ui_config['status_position'][0] * self.ui_config['tile_size'][0], self.ui_config['status_position'][1] * self.ui_config['tile_size'][1]))

        if self.active_ui:
            self.active_ui.render()
            self.surface.blit(self.active_ui.surface, (self.ui_config['left_panel_position'][0] * self.ui_config['tile_size'][0], self.ui_config['left_panel_position'][1] * self.ui_config['tile_size'][1]))

    def get_tile(self, index):
        return self.tile_set[index]