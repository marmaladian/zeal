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
    
    def __init__(self, size: tuple[int, int], list_items: list, title = None):
        """List items must have a _.label_ string property."""
        self.list_items = []
        self.size = size
        self.title = title
        self.cursor = 0
        if list_items:
            for li in list_items:
                checkbox = UI_Checkbox((0, 0), li)
                checkbox.render()
                self.list_items.append(checkbox)

    def toggle(self):
        self.list_items[self.cursor].toggle()
    
    def up(self):
        self.cursor = max(0, min(self.cursor - 1, len(self.list_items) - 1))

    def down(self):
        self.cursor = max(0, min(self.cursor + 1, len(self.list_items) - 1))
        
    def render(self):
        # TODO move ui_text creation to uimanager
        # TODO don't recreate text each time the menu is re-rendered, cache it
        uitext = UIText(pg.image.load('img/text_atlas.png'), (8, 8))
        uitext_inv = UIText(pg.image.load('img/text_atlas_inv.png'), (8, 8))
        if self.title:
            self.surface = pg.Surface((self.size[0] * 8, (len(self.list_items) + 2) * 8))
        else:
            self.surface = pg.Surface((self.size[0] * 8, len(self.list_items) * 8))
        
        self.surface.fill(pg.Color(12, 16, 28, 0))

        if self.title:
            title_text = uitext.create_surface(self.title, self.size[0])
            self.surface.blit(title_text, (0, 0))

        cursor = uitext.create_surface('>', self.size[0])
        row = 0
        if self.list_items:
            for item in self.list_items:
                if row == self.cursor:
                    self.surface.blit(cursor, (0, (row + 2) * 8))
                if item.checked:
                    t = uitext_inv.create_surface(item.label, self.size[0] - 2)
                else:
                    t = uitext.create_surface(item.label, self.size[0] - 2)
                if self.title:
                    self.surface.blit(t, (2 * 8, (row + 2) * 8))
                else:
                    self.surface.blit(t, (2 * 8, row * 8))
                row += 1
            

    def values(self):
        # return the checked state of all the items
        pass

