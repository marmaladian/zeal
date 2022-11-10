import random
from actions import *
import pygame as pg
from pygame.locals import *
from actor import Actor

class Monster(Actor):

    def __init__(self, tile_id) -> None:
        super().__init__(tile_id)
        self.action_list = [ActionWalk(self, ( 0, -1,  0)),
                            ActionWalk(self, ( 0,  1,  0)),
                            ActionWalk(self, (-1,  0,  0)),
                            ActionWalk(self, ( 1,  0,  0))
                            # ActionWalk(self, ( 0,  0,  1)),
                            # ActionWalk(self, ( 0,  0, -1))
                            ]

    def next_action(self, world: World):
        return random.choice(self.action_list)
            
    
                    

                    
                    
                    
                    