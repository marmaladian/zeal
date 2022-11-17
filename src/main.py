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

    tile_graphics = {}
    bs = {}

    # LOAD TEST TILES

    for graphic in config.graphics:
        tile = UITile(graphic['name'], ui_config['tile_size'], graphic['data'])
        tile_graphics[graphic['name']] = tile

    for block in config.tiles:
        b = Block(block['name'], block['tile'], block['colours'], block['walkable'])
        bs[block['name']] = b

    player = Player('player')

    world = World()
    test_map = Map(bs, bs['border'], (21, 16))
    test_map.set_random((21, 16))
    test_map.add_actor(player)
    test_map.load(config.test_map_array)
    test_map.layers[0].items = { (0, 0): ['a tomato', 'chutney', 'an oily, peppery soup'],
                                 (8, 8): ['hat', 'turnip', 'a pinch of spice']}
    test_map.layers[1].items = { (15, 5): ['a white gourd', '12 copper coins'] }
    for _ in range(4):
        monster = Monster('monster')
        test_map.add_actor(monster)
    world.set_current_map(test_map)
    world.next_actor()

    ui_mgr = UIManager(screen_buffer, ui_config, tile_graphics)

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
                    if event.key == K_x:
                        selected_items = ui_mgr.active_ui.activate()
                        if selected_items:
                            player.set_next_action( ActionPickup(player, selected_items) )
                            ui_mgr.active_ui = None
                            ui_mode = False
                    if event.key == K_z:
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
                        # cancel/map move
                        pass
                    if event.key == K_x:
                        # confirm/activate/menu
                        x, y, z = player.position
                        # if items, pop up ui
                        items = world.map.layers[z].items.get((x, y))
                        if items:                            
                            ui_mgr.active_ui = UI_CheckboxList(ui_mgr, ui_mgr.ui_config['left_panel_size'], items, 'PICK UP?')
                            ui_mode = True
                        # if stairs, go up/down
                        elif world.map.tile_at((x, y, z)).name == 'stairs_down':
                            player.set_next_action( ActionWalk(player, (0, 0, -1)) )
                        elif world.map.tile_at((x, y, z)).name == 'stairs_up':
                            player.set_next_action( ActionWalk(player, (0, 0,  1)) )        
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