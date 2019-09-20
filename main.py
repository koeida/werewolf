import curses
from wlib import *
from random import randint, choice

from display import *

m = [[2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]



def main(screen):
    inp = 0 
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    player = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "w", 1, 3)
    cs = [player]
    
    news.append("WELCOME TO WEREWOLF")

    for x in range(10):
        villager = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "v", 5, mode="wander")
        cs.append(villager)
        
    for x in range(5):
        guard = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "g", 5, mode="wander")
        cs.append(guard)
        
    for x in range(35):
        (building_x, building_y, building) = random_building()
        stamp_building(building_x, building_y, building, m)        
    
    objects = gen_objects(m)
    coin = Object(randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT), "$", 11, "a coin", "oooh, a coin")
    player.inventory.append(coin)
    
    while(inp != 113): # Quit game if player presses "q"
        screen.clear()
        
        keyboard_input(inp, player, m, cs, objects)
        
        draw_map(screen, tiles, m)
        
        for o in objects:
            screen.addstr(o.y, o.x, o.icon,curses.color_pair(o.color))
            
        for c in cs:
            if c.stun_timer == 0:
                if c.icon == "v":
                    move_villager(c,player,m,cs,objects)
                elif c.icon == "g":
                    move_guard(c,player,m,cs,objects)

            if c.stun_timer != 0:
                c.stun_timer -= 1

        if player.hp == 0:
            return
        # display callz
        for c in cs:
            screen.addstr(c.y, c.x, c.icon, curses.color_pair(c.color))
            
        display_news(screen, news)
        
        display_inv(screen, player.inventory)
        
        display_hp(screen, player.hp)            
            
        screen.refresh()

        inp = screen.getch()
        
curses.wrapper(main)