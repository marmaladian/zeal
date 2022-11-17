import pygame as pg
from ui.ui_manager import UIManager

from ui.ui_text import UIText

class UIControl:

    def __init__(self, ui: UIManager) -> None:
        self.ui = ui

class UI_Checkbox(UIControl):

    def __init__(self, ui: UIManager, position: tuple[int, int], label = 'UNKNOWN', refers_to = None) -> None:
        self.checked = False
        self.position = position
        self.refers_to = refers_to
        self.update_size()
        self.surface = pg.Surface(self.size)
        self.label = label
        super().__init__(ui)

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
    
    def __init__(self, ui: UIManager, size: tuple[int, int], list_items: list, title = None):
        self.list_items = []
        self.size = size
        self.title = title
        self.cursor = 0
        if list_items:
            for li in list_items:
                checkbox = UI_Checkbox(ui, (0, 0), li, li)
                checkbox.render()
                self.list_items.append(checkbox)
        super().__init__(ui)

    def activate(self):
        if self.cursor == len(self.list_items): # cursor is on OK button
            return self.get_checked()
        else:
            self.list_items[self.cursor].toggle()
            return None
    
    def up(self):
        self.cursor = max(0, min(self.cursor - 1, len(self.list_items)))

    def down(self):
        self.cursor = max(0, min(self.cursor + 1, len(self.list_items)))
        
    def render(self):
        # TODO move ui_text creation to uimanager
        # TODO don't recreate text each time the menu is re-rendered, cache it

        offset = 2 if self.title else 0

        self.surface = pg.Surface((self.size[0] * 8, (len(self.list_items) + offset + 2) * 8)) # +2 is for the gap and then OK button
        
        self.surface.fill(pg.Color(12, 16, 28, 0))

        if self.title:
            title_text = self.ui.text_normal.create_surface(self.title, self.size[0])
            self.surface.blit(title_text, (0, 0))

        cursor = self.ui.text_normal.create_surface('>', self.size[0])
        confirm = self.ui.text_normal.create_surface('OK', self.size[0])
        confirm_inv = self.ui.text_invert.create_surface('OK', self.size[0])

        row = 0
            
        if self.list_items:
            for item in self.list_items:
                if row == self.cursor:
                    self.surface.blit(cursor, (0, (row + 2) * 8))
                if item.checked:
                    t = self.ui.text_invert.create_surface(item.label, self.size[0] - 2)
                else:
                    t = self.ui.text_normal.create_surface(item.label, self.size[0] - 2)
                self.surface.blit(t, (2 * 8, (row + offset) * 8))
                row += 1
            # draw OK button
            if self.cursor == len(self.list_items):
                self.surface.blit(confirm_inv, (0, (row + 1 + offset) * 8))
            else:
                self.surface.blit(confirm, (0, (row + 1 + offset) * 8))


    def get_checked(self):
        checked_items = []
        for checkbox in self.list_items:
            if checkbox.checked:
                checked_items.append(checkbox.refers_to) 
        print('checked:', checked_items)
        return checked_items
        

