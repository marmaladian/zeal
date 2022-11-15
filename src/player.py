from actions import *
import pygame as pg
from pygame.locals import *

from actor import Actor

class Player(Actor):

    def __init__(self, tile_id) -> None:
        self.next_action = None
        super().__init__(tile_id)

    def set_next_action(self, action: Action):
        self.next_action = action

    def get_next_action(self):
        action = self.next_action
        self.next_action = None
        return action