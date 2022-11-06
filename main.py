# carrot sticks
# 

import pygame as pg
from pygame.locals import *
from tile import Tile
from tileset import TileSet
from tilemap import TileMap
from mob import Mob

def main():

    zoom_scale = 3

    pg.init()
    pg.display.set_caption('zeal')
    screen = pg.display.set_mode((8 * 32 * zoom_scale, 8 * 20 * zoom_scale))
    screen_buffer = pg.Surface((8 * 32, 8 * 20))

    t1 = Tile(pg.image.load('img/test_dot.png'), True)
    t2 = Tile(pg.image.load('img/test_fish.png'), True)
    t3 = Tile(pg.image.load('img/test_skull.png'), True)

    t4 = Tile(pg.image.load('img/test_water.png'), False)
    t5 = Tile(pg.image.load('img/test_wall.png'), False)

    t6 = Tile(pg.image.load('img/test_blank.png'), True)
    t7 = Tile(pg.image.load('img/test_dots.png'), True)

    ts = TileSet()
    ts.add(t1)
    ts.add(t2)
    ts.add(t3)
    ts.add(t4)
    ts.add(t5)
    ts.add(t6)
    ts.add(t7)

    # border tile
    t0 = Tile(pg.image.load('img/test_blank.png'), False)

    tm = TileMap(ts, t0, (32, 20))
    tm.set_random()
    tm.render()

    player_tile = Tile(pg.image.load('img/test_player.png'), False)
    player = Mob(tm)
    player.set_tile(player_tile)

    # the tileset contains an instance of each tile (pattern+colour way+game_properties)
    # a tilemap references the tileset (indexes)
    # a world consists of many locations
    # a location could be procedural or predefined.
    # a location consists of layers (z-height)
    # each layer has a tilemap, object list, mob list.
    # two mobs cannot occupy the same space.
    # many objects can be on the same square (only one is displayed)
    # a mob can be on the same square as an object.
    # the game iterates through the mobs, and other events (e.g. weather, dynamic events) in order of speed.
    # when it is the player's turn, the game waits.


    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    player.move((0, -1))
                if event.key == K_s:
                    player.move((0, 1))
                if event.key == K_a:
                    player.move((-1, 0))
                if event.key == K_d:
                    player.move((1, 0))
        # screen_buffer.fill((232, 233, 217))
        
        screen_buffer.blit(tm.surface, (0, 0))
        player.draw(screen_buffer)
        pg.transform.scale(screen_buffer, screen.get_size(), screen)

        

        pg.display.flip()
    

if __name__=="__main__":
    main()