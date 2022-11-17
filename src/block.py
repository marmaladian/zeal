import pygame as pg
import numpy as np

class Block:
    size = (8, 8)    # pixel size of tiles

    def __init__(self, name, tile, colours: tuple[int, int], walkable : bool) -> None:
        self.name = name
        self.tile = tile
        self.colours = colours
        self.walkable = walkable