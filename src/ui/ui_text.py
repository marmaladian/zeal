import pygame as pg
import math

class UIText:
    # TODO can intern be used to improve this?

    default_mapping = ['01234567890',
                       'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                       'abcdefghijklmnopqrstuvwxyz',
                       ' .,?<>']

    def __init__(self, atlas: pg.Surface, char_size: tuple[int, int] = (8, 8), mapping = None):
        
        if mapping is None:
            self.mapping = UIText.default_mapping
        else:
            self.mapping = mapping

        self.atlas = atlas
        self.char_size = char_size

        # generate dictionary of char: rect
        self.chars = {}
        atlas_row = 0
        for row in self.mapping:
            atlas_col = 0
            for char in row:
                char_surface = pg.Surface(self.char_size)
                char_surface.blit(self.atlas, (0, 0), (atlas_col *  self.char_size[0], atlas_row * self.char_size[1], self.char_size[0], self.char_size[1]))
                self.chars[char] = char_surface
                atlas_col += 1
            atlas_row += 1

    def create_surface(self, text: str, wrap: int = 0) -> pg.Surface:
        # TODO handle splitting on spaces... this is going to be more complicated
        # than i thought
        if wrap > 0:
            width = min(len(text), wrap)
            height = math.ceil(len(text) / width)
        else:
            width = len(text)
            height = 1

        s = pg.Surface((width * self.char_size[0], height * self.char_size[1]))
        #s.fill(pg.Color(236, 71, 0))
        row, col = (0, 0)
        for char in text:
            s.blit(self.chars[char], (col * self.char_size[0], row * self.char_size[1]))
            col += 1
            if col > width:
                col = 0
                row += 1
        return s