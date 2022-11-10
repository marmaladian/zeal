import pygame as pg

class UIText:
    # TODO can intern be used to improve this?

    text_atlas = pg.image.load('img/text_atlas.png')
    

    def __init__(self, text: str, wrap: int = -1) -> None:
        # todo handle splitting on spaces... god, this is going to be more complicated
        # than i thought
        width = len(text)
        return UIText.text_atlas