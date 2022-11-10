class UIControl:

    def __init__(self, label = None) -> None:
        self.label = label

class UI_Checkbox(UIControl):

    def __init__(self, position: tuple[int, int], label = None) -> None:
        self.checked = False
        self.position = position
        self.update_size()
        self.surface = pg.Surface(self.size)
        super().__init__()

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
        width = len(self.label) * 8 # TODO remove magic number
        self.size = (width, 8)

    def render(self):
        



class UI_CheckboxList(UIControl):
    
    def __init__(self, position: tuple[int, int], list_items: list):
        """List items must have a ui_label property."""
        self.list_items = []
        self.position = position
        for li in list_items:
            checkbox = UI_Checkbox(li.ui_label)
            checkbox.render()
            self.list_items.append(checkbox)
        
    def render(self):
        self.surface = None
        # blit all the individual checkboxes onto the larger surface

    def values(self):
        # return the checked state of all the items
        pass

