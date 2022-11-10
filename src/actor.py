from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from world import World

from block import Block


class Actor:

# breed("goblin peon", lightBrown, 16, [
#   attack("stab[s]", 6)
# ], drop: [
#   chanceOf(10, "spear:3"),
#   chanceOf(5, "healing:2"),
# ], meander: 2, flags: "few open-doors");

    def __init__(self, tile_id) -> None:
        self.tile_id = tile_id
        self.position = (1, 1, 0)
        self.inventory = []

    def next_action(self, world: World):
        # for player, get UI action
        # for monster, AI action
        pass

    # def move(self, offset):
    #     new_position = self.position[0] + offset[0], self.position[1] + offset[1]
    #     if self.can_move_to(new_position):
    #         self.position = new_position

    # TODO move these to the action

    def is_traversable(self, tile: Block):
        # if flying/walking/swimmer, check different things.
        return tile.walkable

    def can_move_to(self, world: World, position: tuple[int, int, int]):
        return self.is_traversable(world.map.tile_at(position))
