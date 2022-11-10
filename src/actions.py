from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from actor import Actor

from world import World

class Action:

    def __init__(self) -> None:
        pass

    def perform():
        pass

class ActionWalk(Action):

    def __init__(self, subject: Actor, direction: tuple[int, int, int]) -> None:
        self.subject = subject
        self.direction = direction
        super().__init__()

    def perform(self, world: World):
        target_position = (self.subject.position[0] + self.direction[0], 
                           self.subject.position[1] + self.direction[1],
                           self.subject.position[2] + self.direction[2]) 
        
        if self.subject.can_move_to(world, target_position):
            self.subject.position = target_position

class ActionPickup(Action):

    def __init__(self, subject: Actor, items) -> None:
        self.subject = subject
        self.items = items # a list of items, passed from the UI or the monster AI
        super().__init__()

    def perform(self, context):
        print('picking up ', self.items)
        # remove the items from the subject's cell
        # add the items to the subject's inventory.
        pass
        # if type(self.subject) is Player:
            # check if there are any items there.
            # 
            # if not, failure.

        # if monster, allow them to select what items they pick up.

class ActionQuit(Action):
    
    def __init__(self):
        super().__init__()
    
    def perform(self, context):
        pass