import numpy as np
from actor import Actor
from block import Block

class MapLayer:

    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.terrain = np.zeros(size, dtype=int)    
        self.items = {}

    def set_random(self, block_set : list[Block]):
        n = len(block_set)
        self.terrain = np.random.randint(n, size=self.size)

    def load(self, array: np.ndarray):
        array = array.T
        self.size = array.shape
        self.terrain = array

class Map:

    def __init__(self, block_set: list[Block], border_tile: Block, size: tuple[int, int]) -> None:
        self.size = size
        self.layers = []
        self.actors = []
        self.block_set = block_set
        self.border_tile = border_tile

    def add_layers(self, layers: list[MapLayer]) -> None:
        self.layers.append(layers)

    def add_actor(self, actor) -> None:
        self.actors.append(actor)

    def load(self, array: np.ndarray):
        z, y, x = array.shape
        self.size = (x, y)
        self.layers = []
        for layer in range(z):
            l = MapLayer(self.size)
            l.load(array[layer])
            self.layers.append(l)
    
    def set_random(self, size: tuple[int, int], num_layers: int = 3):
        self.size = size
        for _ in range(num_layers):
            l = MapLayer(self.size)
            l.set_random(self.block_set)
            self.add_layers(l)

    def tile_at(self, position: tuple[int, int, int]) -> Block:
        x, y, z = position
        if (0 <= x < self.size[0]) and (0 <= y < self.size[1]) and (0 <= z < len(self.layers)):
            return self.block_set[self.layers[z].terrain[x, y]]
        else:
            return self.border_tile

class World:

    def __init__(self) -> None:
        self.turn = 0
        self.time = 0
        self.next_actor_index = 0
        self.curr_actor = None

    def set_current_map(self, map: Map) -> None:
        self.map = map

    def next_actor(self) -> Actor:
        self.curr_actor = self.map.actors[self.next_actor_index]
        self.next_actor_index = (self.next_actor_index + 1) % len(self.map.actors)
        