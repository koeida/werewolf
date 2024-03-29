import curses
from wlib import *
from random import randint, choice

from display import *
from mapgen import village, gen_objects, build_world
import mapgen


def on_cam(t, cam_x, cam_y):
    if t.x < cam_x + CAM_WIDTH and t.y < cam_y + CAM_HEIGHT:
        if t.x > cam_x and t.y > cam_y:
            return True
    return False
    
def make_world():
    m = [[2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

    player = Creature(333, 333, "w", 1, 3)
    cs = [player]
    
    news.append("WELCOME TO WEREWOLF")

    for x in range(int(MAP_AREA * 0.002) ): #10
        villager = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "v", 5, mode="wander")
        #cs.append(villager)
        
    for x in range(int(MAP_AREA * 0.0006)):
        guard = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "g", 5, mode="wander")
        #cs.append(guard)

    #factory(m, 2, 2, 80, 80)
    #village(m, 82 ,2 ,162 ,80)
    build_world(mapgen.zones, m)

    for row in m:
        for x in row:
            if x not in range(0,10):
                print(x)
                exit()

    objects = gen_objects(m)
    coin = Object(randint(1, MAP_WIDTH), randint(1, MAP_HEIGHT), "$", 11, "a coin", "oooh, a coin")
    player.inventory.append(coin)
    return (m, player, objects, cs)

def main(screen, world):
    inp = 0 
    curses.curs_set(False) # Disable blinking cursor
    init_colors()
    
    m, player, objects, cs = world
    
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
            if c.stun_timer == 0 and distance(c, player) <= CAM_WIDTH:
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

        
world = make_world()
curses.wrapper(main, world)
