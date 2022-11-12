import pygame as pg

from ui.ui_text import UIText

class UIControl:

    def __init__(self, label = None) -> None:
        self.label = label

class UI_Checkbox(UIControl):

    def __init__(self, position: tuple[int, int], label = None) -> None:
        self.checked = False
        self.position = position
        self.update_size()
        self.surface = pg.Surface(self.size)
        super().__init__(label)

    def value(self):
        return self.checked

    def toggle(self):
        self.checked = not self.checked

    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def set_check(self, checked: bool):
        self.checked = checked

    def set_label(self, label):
        self.label = label
        self.update_size()
        self.surface = pg.Surface(self.size)
        self.render()

    def update_size(self):
        width = len(self.__str__()) * 8 # TODO remove magic number
        self.size = (width, 8)

    def render(self):
        pass

class UI_CheckboxList(UIControl):
    
    def __init__(self, position: tuple[int, int], list_items: list):
        """List items must have a __str__ property."""
        self.list_items = []
        self.position = position
        if list_items:
            for li in list_items:
                checkbox = UI_Checkbox((0, 0), li)
                checkbox.render()
                self.list_items.append(checkbox)
        
    def render(self):
        uitext = UIText(None, (8, 8))
        if self.list_items:
            self.surface = pg.Surface((14 * 8, len(self.list_items) * 8))
            row = 0
            for item in self.list_items:
                t = uitext.create_surface(item.label, 14)
                self.surface.blit(t, (0, row * 8))
                row += 1

    def values(self):
        # return the checked state of all the items
        pass

