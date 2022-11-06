from tile import Tile
from pygame import Surface

from tilemap import TileMap

class Mob:

    def __init__(self, map : TileMap) -> None:
        self.map = map
        self.position = (1, 1)

    def set_tile(self, tile: Tile):
        self.tile = tile

    def draw(self, canvas: Surface):
        self.tile.draw(canvas, self.position)

    def move(self, offset):
        new_position = self.position[0] + offset[0], self.position[1] + offset[1]
        if self.can_move_to(new_position):
            self.position = new_position 

    def is_traversable(self, tile: Tile):
        # if flying/walking/swimmer, check different things.
        return tile.walkable

    def can_move_to(self, position: tuple[int, int]):
        return self.is_traversable(self.map.tile_at(position))
