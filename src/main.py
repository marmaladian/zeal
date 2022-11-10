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

import pygame as pg
import numpy as np
from pygame.locals import *
from actions import Action, ActionQuit
from player import Player
from block import Block
from actor import Actor
from monster import Monster
from ui.ui_manager import UIManager
from ui.ui_tile import UITile
from ui.ui_tilemap import UITileMap
from world import Map, World

def main():

    zoom_scale = 3

    pg.init()
    pg.display.set_caption('zeal')
    screen = pg.display.set_mode((8 * 23 * zoom_scale, 8 * 18 * zoom_scale))
    screen_buffer = pg.Surface((8 * 23, 8 * 18))

    # ui tileset and blockset
    ts = []
    bs = []

    def create_block_and_tile(name: str, walkable: bool, img_path: str) -> None:
        block = Block(name, walkable)
        tile = UITile(name, pg.image.load(img_path))
        bs.append(block)
        ts.append(tile)

    create_block_and_tile('border', False, 'img/test_border.png')
    create_block_and_tile('blank', True, 'img/test_blank.png')
    create_block_and_tile('dot', True, 'img/test_dot.png')
    create_block_and_tile('fish', True, 'img/test_fish.png')
    create_block_and_tile('skull', True, 'img/test_skull.png')
    create_block_and_tile('water', False, 'img/test_water.png')
    create_block_and_tile('wall', False, 'img/test_wall.png')
    create_block_and_tile('dots', True, 'img/test_dots.png')
    create_block_and_tile('stairs', True, 'img/test_stairs.png')
    create_block_and_tile('grass', True, 'img/test_grass.png')
    create_block_and_tile('stagger', True, 'img/test_stagger.png')
    create_block_and_tile('grid', True, 'img/test_grid.png')
    create_block_and_tile('door', True, 'img/test_door.png')
    create_block_and_tile('tuft', True, 'img/test_tuft.png')
    create_block_and_tile('bridge_left', False, 'img/test_bridge_left.png')
    create_block_and_tile('bridge_right', False, 'img/test_bridge_right.png')
    create_block_and_tile('bridge_shadow', False, 'img/test_bridge_shadow.png')
    create_block_and_tile('waves', False, 'img/test_waves.png')
    create_block_and_tile('water_bank', False, 'img/test_water_bank.png')
    create_block_and_tile('wall_top', False, 'img/test_wall_top.png')
    create_block_and_tile('wall_thin', False, 'img/test_wall_thin.png')
    create_block_and_tile('bench_n_end', False, 'img/test_bench_n_end.png')
    create_block_and_tile('bench_ns', False, 'img/test_bench_ns.png')
    create_block_and_tile('bench_sw_corner', False, 'img/test_bench_sw_corner.png')
    create_block_and_tile('bench_ew', False, 'img/test_bench_ew.png')
    create_block_and_tile('wall_top_full', False, 'img/wall_top_full.png')
    create_block_and_tile('stairs_up', True, 'img/test_stairs_up.png')
    create_block_and_tile('tree_1_bottom', False, 'img/test_tree_1_bottom.png')
    create_block_and_tile('tree_1_top', False, 'img/test_tree_1_top.png')
    create_block_and_tile('pot', False, 'img/test_pot.png')
    create_block_and_tile('tree_2_bottom', False, 'img/test_tree_2_bottom.png')
    create_block_and_tile('tree_2_top', False, 'img/test_tree_2_top.png')
    create_block_and_tile('sky', False, 'img/test_sky.png') #32

    player_tile = UITile('player', pg.image.load('img/test_player.png'))
    ts.append(player_tile)
    player = Player(len(ts) - 1)

    monster_tile = UITile('monster', pg.image.load('img/test_monster.png'))
    ts.append(monster_tile)
    

    test_map_array = np.array([[[1, 5, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5],
                                [1, 5, 5, 5, 5, 1, 1, 1,31,25,19,19,19,19,19,19,25, 1, 5, 5, 5],
                                [1, 5, 5, 5, 5, 1,28, 1,30,25, 6,12, 6, 6, 6, 6,25, 1, 1, 1, 1],
                                [1, 5, 5, 5, 5, 1,27, 1, 1,25, 7, 1, 1, 1, 1,29,25, 1, 1, 2, 1],
                                [1, 5, 5, 5, 5, 1,19,19,19,19, 2, 1, 2,21, 1, 1,25, 1,14,16,16],
                                [1, 5, 5, 5, 5, 2, 6, 6, 6, 6, 1, 1, 7,22, 1, 1,25, 1, 5, 5, 5],
                                [2, 2, 2, 13,2, 2, 1,29, 1, 1, 1, 1, 1,23,24,24,25, 1, 5, 5, 5],
                                [2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 2, 1, 1, 2, 1, 1,25,13, 5, 5, 5],
                                [2,14,16,16,15, 1,25, 2, 2, 2, 2, 1, 1, 1, 1,26,25, 1, 5, 5, 5],
                                [2, 5, 5, 5, 5, 1,19,19,19,19, 1, 1,19,19,19,19,19, 1, 5, 5, 5],
                                [2, 5, 5, 5, 5, 1, 6, 6, 6, 6, 1, 1,20,20,20,20,20, 1, 5, 5, 5],
                                [1,17, 5,17, 5, 1, 1, 9, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 5, 5, 5],
                                [1, 5, 5,17,17, 1, 4, 1, 1, 7, 2, 1, 1, 1,18,18,18,18, 5, 5, 5],
                                [1, 5, 5, 5, 5, 3, 1, 1, 1, 1, 1, 2, 1, 1, 5, 5, 5, 5, 5, 5, 5],
                                [1, 5, 5, 5, 5,18,18,18,18,18, 2, 2,18,18, 5, 5, 5, 5, 5, 5, 5],
                                [1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5]],

                               [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25,19,19,19,19,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25,20,20,20,20,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25, 2, 2, 2, 2,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25,29, 2, 2, 2,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25,29, 2, 2, 2,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25, 2, 2, 2, 2,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25, 2, 2, 2, 2,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,25, 2,29, 2, 8,25, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,19,19,19,19,19,19, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,20,20,20,20,20,20, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],

                               [[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25,19,19,19,19,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25,20,20,20,20,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25, 2, 2, 2, 2,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25,29, 2, 2, 2,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25,29, 2, 2, 2,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25, 2, 2, 2, 2,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25, 2, 2, 2, 2,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,25, 2,29, 2, 8,25,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,19,19,19,19,19,19,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,20,20,20,20,20,20,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32],
                                [32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32]]])

    print(test_map_array.shape)
    print(test_map_array[0])

    world = World()
    test_map = Map(bs, bs[0], (21, 16))
    test_map.set_random((21, 16))
    test_map.add_actor(player)
    test_map.load(test_map_array)
    for _ in range(4):
        monster = Monster(len(ts) - 1)
        test_map.add_actor(monster)
    world.set_current_map(test_map)
    world.next_actor()

    ui = UIManager((34, 23), ts, (8, 8), (32, 21))

    running = True
    action: Action = None

    while running:
  
        while not action:
            action = world.curr_actor.next_action(world)
        if type(action) is ActionQuit:
            running = False
        else:
            action.perform(world)
            world.next_actor()
            # this can return success or failure - if it fails, player can try another action.
        action = None

        # RENDER

        # TODO treat map view as portal - i.e. render region of it
        # TODO move old TileMap stuff into a UI thing
        # TODO split tiles from sprites
        
        ui.render(world.map, player.position[2])
        screen_buffer.blit(ui.surface, (0, 0))
        # player.draw(screen_buffer)
        
        # RESIZE
        pg.transform.scale(screen_buffer, screen.get_size(), screen)
        pg.display.flip()
    

if __name__=="__main__":
    main()