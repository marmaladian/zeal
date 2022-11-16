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
            return (True, None)
        else:
            return (False, None)

class ActionPickup(Action):

    def __init__(self, subject: Actor, items) -> None:
        self.subject = subject
        self.items = items # a list of items, passed from the UI or the monster AI
        super().__init__()

    def perform(self, world: World):
        if self.items:
            self.subject.inventory.append(self.items)
            world.map.layers[self.subject.position[2]].items[(self.subject.position[0], self.subject.position[1])] = [i for i in world.map.layers[self.subject.position[2]].items[(self.subject.position[0], self.subject.position[1])] if (i not in self.items)]
            if world.map.layers[self.subject.position[2]].items[(self.subject.position[0], self.subject.position[1])] == []:
                print('removing item entry for position')
                world.map.layers[self.subject.position[2]].items.pop((self.subject.position[0], self.subject.position[1]))
            return (True, f'You pick up the {self.items}.')
        else:
            return (False, 'There is nothing here to pick up OR you pick up nothing.')