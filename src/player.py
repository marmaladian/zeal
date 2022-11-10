from actions import *
import pygame as pg
from pygame.locals import *

from actor import Actor


class Player(Actor):

    def __init__(self, tile_id) -> None:
        super().__init__(tile_id)

    def next_action(self, world: World):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return ActionQuit()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    return ActionWalk(self, (0, -1, 0))
                if event.key == K_s:
                    return ActionWalk(self, (0, 1, 0))
                if event.key == K_a:
                    return ActionWalk(self, (-1, 0, 0))
                if event.key == K_d:
                    return ActionWalk(self, (1, 0, 0))
                if event.key == K_q:
                    return ActionWalk(self, (0, 0, 1))
                if event.key == K_z:
                    return ActionWalk(self, (0, 0, -1))
                if event.key == K_COMMA:
                    print('pick up')
                    x, y, z = self.position
                    items = world.map.layers[z].items.get((x, y))
                    # show UI for pickup
                    # but first we'll just pickup everything at the site

                    # return a list of items or None
                    # if list is empty, return None
                    # else return ActionPickup(self, position, itemlist)
                    # items = ['cod liver oil', 'foot long steamed dim sim']
                    return ActionPickup(self, items)