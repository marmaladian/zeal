# picking up items
#  - object map
# multiple locations
# vertical movement
# scrolling maps/viewport
# animated tiles
# weather effects/animation
# attacking
# gui
# text engine

import sys
from datetime import datetime
import pygame as pg
import numpy as np
from pygame.locals import *
from actions import *
from player import Player
from block import Block
from actor import Actor
from monster import Monster
from ui.ui_manager import UIManager
from ui.ui_tile import UITile
from ui.ui_tilemap import UITileMap
from ui.ui_controls import UI_CheckboxList
from world import Map, World
import config

def main():

    # TODO make this like: 'map': { 'size': (blah, blah), 'alignment': centred}, 'panel': {'size': (23, 2), 'alignment':'bottom-left' (then ref some other object to snap it to)}
    ui_config = {
        'screen_size':          (55, 36),
        'map_size':             (21, 16),
        'left_panel_size':      (21, 16),        
        'left_margin':          2,
        'right_margin':         2,
        'gutter':               1,
        'tile_size':            (8, 8),
        'zoom_scale':           3
    }

    ui_config['top_margin'] =           int((1/3) * (ui_config['screen_size'][1] - ui_config['map_size'][1]))
    ui_config['bottom_margin'] =        ui_config['screen_size'][1] - ui_config['map_size'][1] - ui_config['top_margin']
    ui_config['left_panel_position'] =  (ui_config['left_margin'], ui_config['top_margin'])
    ui_config['map_position'] =         (ui_config['left_margin'] + ui_config['left_panel_size'][0] + ui_config['gutter'], ui_config['top_margin'])
    ui_config['status_position'] =      (ui_config['map_position'][0], ui_config['map_position'][1] + ui_config['map_size'][1] + 1)

    pg.init()
    pg.display.set_caption(f'Zeal — {datetime.now().strftime("%d-%b-%Y %-I:%M:%S %p")}')
    screen = pg.display.set_mode((ui_config['tile_size'][0] * ui_config['screen_size'][0] * ui_config['zoom_scale'], ui_config['tile_size'][1] * ui_config['screen_size'][1] * ui_config['zoom_scale']))
    screen_buffer = pg.Surface((ui_config['tile_size'][0] * ui_config['screen_size'][0], ui_config['tile_size'][1] * ui_config['screen_size'][1]))
    
    # ui tileset and blockset

    ts = []
    bs = []

    # LOAD TEST TILES

    for tile in config.test_tiles:
        block = Block(tile['name'], tile['walkable'])
        #tile = UITile(tile['name'], pg.image.load(tile['image']))
        tile = UITile(tile['name'], ui_config['tile_size'], tile['data'])
        bs.append(block)
        ts.append(tile)

    player = Player(34)

    world = World()
    test_map = Map(bs, bs[0], (21, 16))
    test_map.set_random((21, 16))
    test_map.add_actor(player)
    test_map.load(config.test_map_array)
    for _ in range(4):
        monster = Monster(35)
        test_map.add_actor(monster)
    world.set_current_map(test_map)
    world.next_actor()

    ui_mgr = UIManager(screen_buffer, ui_config, ts)

    running = True
    action: Action = None

    ui_mgr.render(world.map, player.position[2])
    screen_buffer.blit(ui_mgr.surface, (0, 0))
    ui_mode = False

    # RESIZE
    pg.transform.scale(screen_buffer, screen.get_size(), screen)
    pg.display.flip()

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if ui_mode:
                    if event.key == K_UP:
                        ui_mgr.active_ui.up()
                    if event.key == K_DOWN:
                        ui_mgr.active_ui.down()
                    if event.key in [K_SPACE, K_RETURN]:
                        ui_mgr.active_ui.toggle()
                    if event.key == K_ESCAPE: # TODO how to move this to the point where the UI is summoned?
                        selected_items = ui_mgr.active_ui.get_checked()
                        player.set_next_action( ActionPickup(player, selected_items) )
                        ui_mgr.active_ui = None
                        ui_mode = False
                else:       # get player char input
                    # TODO move this to player event handler fn
                    if event.key == K_UP:
                        player.set_next_action( ActionWalk(player, (0, -1, 0)) )
                    if event.key == K_DOWN:
                        player.set_next_action( ActionWalk(player, (0, 1, 0)) )
                    if event.key == K_LEFT:
                        player.set_next_action( ActionWalk(player, (-1, 0, 0)) )
                    if event.key == K_RIGHT:
                        player.set_next_action( ActionWalk(player, (1, 0, 0)) )
                    if event.key == K_q:
                        player.set_next_action( ActionWalk(player, (0, 0, 1)) )
                    if event.key == K_z:
                        player.set_next_action( ActionWalk(player, (0, 0, -1)) )
                    if event.key == K_COMMA:
                        x, y, z = player.position
                        items = world.map.layers[z].items.get((x, y))
                        ui_mgr.active_ui = UI_CheckboxList(ui_mgr, ui_mgr.ui_config['left_panel_size'], items, 'PICK UP?')
                        ui_mode = True
        
        if not ui_mode:
            action = world.curr_actor.get_next_action()

            if action is None:
                continue
            successful, message = action.perform(world)
            if message:
                print(message)
            if successful:
                world.next_actor()

            action = None

        # RENDER
        ui_mgr.render(world.map, player.position[2])
        screen_buffer.blit(ui_mgr.surface, (0, 0))
        
        # RESIZE
        pg.transform.scale(screen_buffer, screen.get_size(), screen)
        pg.display.flip()

if __name__=="__main__":
    main()