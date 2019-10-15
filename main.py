import curses
from wlib import *
from random import randint, choice

from display import *

m = [[2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

def on_cam(t, cam_x, cam_y):
    if t.x < cam_x + CAM_WIDTH and t.y < cam_y + CAM_HEIGHT:
        if t.x > cam_x and t.y > cam_y:
            return True
    return False

def main(screen):
    inp = 0 
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    player = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "w", 1, 3)
    cs = [player]
    
    news.append("WELCOME TO WEREWOLF")

    for x in range(100): #10
        villager = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "v", 5, mode="wander")
        cs.append(villager)
        
    for x in range(5):
        guard = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "g", 5, mode="wander")
        cs.append(guard)
        
    for x in range(int(MAP_HEIGHT * MAP_WIDTH / 200)):
        (building_x, building_y, building) = random_building()
        stamp_building(building_x, building_y, building, m)        
    
    objects = gen_objects(m)
    coin = Object(randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT), "$", 11, "a coin", "oooh, a coin")
    player.inventory.append(coin)
    
    
    while(inp != 113): # Quit game if player presses "q"
        screen.clear()
        
        
        keyboard_input(inp, player, m, cs, objects)

        cam_y = player.y - int(CAM_HEIGHT / 2)
        cam_x = player.x - int(CAM_WIDTH / 2) 
        
        draw_map(screen, tiles, m, cam_x, cam_y)
        
        for o in objects:
            if on_cam(o, cam_x, cam_y):
                screen.addstr(o.y - cam_y, o.x - cam_x , o.icon,curses.color_pair(o.color))
            
        for c in cs:
            if c.stun_timer == 0:
                if c.icon == "v":
                    move_villager(c,player,m,cs,objects)
                elif c.icon == "g":
                    move_guard(c,player,m,cs,objects)

            if c.stun_timer != 0:
                c.stun_timer -= 1

            if c.invisibility_timer != 0:
                c.invisibility_timer -= 1
                c.color = under_color(c, m)
            else:
                c.color = c.original_color

        if player.hp == 0:
            return
        # display callz
        for c in cs:
            if on_cam(c,cam_x,cam_y):
                    screen.addstr(c.y - cam_y, c.x - cam_x, c.icon, curses.color_pair(c.color))
            
        display_news(screen, news)
     
        display_inv(screen, player.inventory)
        
        display_hp(screen, player.hp)            
            
        screen.refresh()

        inp = screen.getch()
        
curses.wrapper(main)
