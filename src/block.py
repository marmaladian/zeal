import pygame as pg
import numpy as np

class Block:
    size = (8, 8)    # pixel size of tiles

    def __init__(self, name, walkable : bool) -> None:
        self.name = name
        self.walkable = walkable