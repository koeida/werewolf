from random import randint, choice
import curses
from math import sqrt
import copy

from display import *
from misc import *
from mapgen import *

news = []

class Creature:
    def __init__(self, x, y, icon, color, mode=""):
        self.x = x
        self.y = y
        self.icon = icon
        self.color = color
        self.mode = mode
        self.flee_timer = 4
        self.inventory = []
        
class Object:
    def __init__(self, x, y, icon, color, description = ""):
        self.icon = icon
        self.x = x
        self.y = y
        self.description = description
        self.color = color
        
def distance(c1,c2):
    a = c1.x - c2.x      
    b = c1.y - c2.y
    c = a**2 + b**2
    
    return sqrt(c)

def can_see(row, start, end, m, objects):   
    inb = between(start,end,m[row]) 
    
    if 1 in inb:
        return False
    else:
        return True

def attempt_move(c, m, xmod, ymod, cs,objects):
    nx = c.x + xmod
    ny = c.y + ymod
    if nx > (MAP_WIDTH - 1) or ny > (MAP_HEIGHT - 1) or nx < 0 or ny < 0:
        cs.remove(c)
        news.append("a villager got away")
        return
    for o in objects:
        if m[ny][nx] == 1 or (o.x == nx and o.y == ny):
            return
    c.x += xmod
    c.y += ymod
    
def pick_direction_fleeing(vx, vy, px, py):
    xmod = 0
    ymod = 0
    
    if vx > px:
        xmod = 1 
    elif vx < px:
        xmod = -1
    if vy > py:
        ymod = 1 
    elif vy < py:
        ymod = -1
      
    if xmod != 0 and ymod != 0:
        if abs(px - vx) <= abs(py - vy):
            ymod = 0
        else:
            xmod = 0
    return (xmod, ymod)
        
def move_villager(v,player,m,cs,objects):
    xmod,ymod = (0,0)
    
    # make a copy of the map
    m = copy.deepcopy(m)
    # Loop over object
    for o in filter(lambda o: o.icon == "?",objects):
        m[o.y][o.x] = 1
    
    if (v.x == player.x and can_see(player.x, player.y, v.y, rotate_list(m,3), objects)
    or (v.y == player.y and can_see(player.y, player.x, v.x, m, objects))):
        v.mode = "fleeing"
        v.flee_timer = 4
    
    if v.mode == "fleeing":
        xmod, ymod = pick_direction_fleeing(v.x, v.y, player.x, player.y)
        v.flee_timer -= 1
        if v.flee_timer == 0:
            v.mode = "wander"
    elif v.mode == "wander":
        xmod = randint(-1,1)
        ymod = randint(-1,1)
        if randint (0,1) == 1:
            xmod = 0
        else:
            ymod = 0
    attempt_move(v, m, xmod, ymod,cs,objects)                            
        
def random_building():
    building_x = randint(2,MAP_WIDTH)
    building_y = randint(2,MAP_HEIGHT)
    building_width = randint(4,15)
    building_height = randint(4,15)
    building = make_building(building_width, building_height)
    return (building_x, building_y, building)

def keyboard_input(inp, player, m, cs, objects):
    oldx = player.x
    oldy = player.y
    if inp == curses.KEY_DOWN:
        player.y += 1        
    elif inp == curses.KEY_UP:
        player.y -= 1
    elif inp == curses.KEY_LEFT:
        player.x -= 1
    elif inp == curses.KEY_RIGHT:        
        player.x += 1
    elif inp == curses.KEY_BACKSPACE:        
        for o in objects:
            if int(distance(player,o)) == 1:
                news.append(o.description)
        
    if m[player.y][player.x] == 1:
        player.x = oldx
        player.y = oldy
    for c in filter(lambda o: o.icon == "$",objects):
        if player.x == c.x and player.y == c.y:
            player.inventory.append(c)
            news.append("you collected a coin")
            objects.remove(c)
    
    vs = filter(lambda c: c.icon == "v", cs)
    for v in vs:
        if player.x == v.x and player.y == v.y:
            news.append("You devour the villager...")
            cs.remove(v)
            body = Object(v.x, v.y, "%",1, "A dead villager. Eeeewwww.")
            objects.append(body)
            for x in range(2):
                coin = Object(randint(1,MAP_WIDTH),randint(1,MAP_HEIGHT),"$",11,"oooh, a coin")
                objects.append(coin) 