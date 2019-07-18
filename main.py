import curses
from wlib import *
from random import randint, choice

m = [[2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

def draw_map(screen, tiles, m):
    for row in range(len(m)):
        for column in range(len(m[0])):
            cur_tile_num = m[row][column]
            cur_tile = tiles[cur_tile_num][0]
            screen.addstr(row, column, cur_tile, curses.color_pair(tiles[cur_tile_num][1]))

def main(screen):
    inp = 0 
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    player = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "w", 1)
    cs = [player]
    
    news.append("WELCOME TO WEREWOLF")

    for x in range(10):
        villager = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "v", 5, "wander")
        cs.append(villager)
        
    for x in range(35):
        (building_x, building_y, building) = random_building()
        stamp_building(building_x, building_y, building, m)        
    
    objects = gen_objects(m)
    
    while(inp != 113): # Quit game if player presses "q"
        screen.clear()
        
        keyboard_input(inp, player, m, cs, objects)
        
        draw_map(screen, tiles, m)
        
        for o in objects:
            screen.addstr(o.y, o.x, o.icon, curses.color_pair(1))
        
        for c in cs:
            if c.icon == "v":
                move_villager(c,player,m,cs,objects)
            screen.addstr(c.y, c.x, c.icon, curses.color_pair(c.color))
            
        display_news(screen, news)
        
        #display inv
        screen.addstr(0, MAP_WIDTH + 1, "Inventory:")
        ci = 1
        for i in player.inventory:
            screen.addstr(ci, MAP_WIDTH + 1, i.icon, 0)
            ci += 1
            
            
        screen.refresh()

        inp = screen.getch()
        
curses.wrapper(main)