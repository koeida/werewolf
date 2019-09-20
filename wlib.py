from math import sqrt
import copy

from display import *
from misc import *
from mapgen import *

news = []

class Creature:
    def __init__(self, x, y, icon, color, hp=0, mode=""):
        self.x = x
        self.y = y
        self.icon = icon
        self.color = color
        self.mode = mode
        self.timer = 4
        self.inventory = []
        self.hp = hp
        self.stun_timer = 0

class Object:
    def __init__(self, x, y, icon, color, name = "", description = ""):
        self.icon = icon
        self.x = x
        self.y = y
        self.description = description
        self.color = color
        self.name = name
        self.effect = lambda x, y: None

def distance(c1, c2):
    a = c1.x - c2.x      
    b = c1.y - c2.y
    c = a**2 + b**2
    
    return sqrt(c)


def can_see(row, start, end, m, objects):   
    inb = between(start, end, m[row])
    
    if 1 in inb:
        return False
    else:
        return True
    
def off_map(nx, ny):
    return nx > (MAP_WIDTH - 1) or ny > (MAP_HEIGHT - 1) or nx < 0 or ny < 0

def attempt_move(c, m, xmod, ymod, cs,objects):
    nx = c.x + xmod
    ny = c.y + ymod
    if off_map(nx,ny):
        if c.icon == "v":
            cs.remove(c)
            news.append("a villager got away")
            return
        elif c.icon == "g":
            return
        elif c.icon == "p":
            return
    else:
        if m[ny][nx] == 1:
            return
        for o in objects:
            if o.x == nx and o.y == ny and o.icon == "?":
                return
        c.x += xmod
        c.y += ymod
      
def pick_direction(cx, cy, px, py):
    xmod = 0
    ymod = 0
    
    if cx > px:
        xmod = 1 
    elif cx < px:
        xmod = -1
    if cy > py:
        ymod = 1 
    elif cy < py:
        ymod = -1
      
    if xmod != 0 and ymod != 0:
        if abs(px - cx) <= abs(py - cy):
            ymod = 0
        else:
            xmod = 0
    return (xmod, ymod)
        
def move_villager(v,player,m,cs,objects):
    xmod,ymod = (0,0)
    m = copy.deepcopy(m)
    for o in filter(lambda o: o.icon == "?",objects):
        m[o.y][o.x] = 1
    
    if (v.x == player.x and can_see(player.x, player.y, v.y, rotate_list(m,3), objects)
    or (v.y == player.y and can_see(player.y, player.x, v.x, m, objects))):
        v.mode = "fleeing"
        v.timer = 4
    
    if v.mode == "fleeing":
        xmod, ymod = pick_direction(v.x, v.y, player.x, player.y)
        v.timer -= 1
        if v.timer == 0:
            #news.append("grrr")
            v.mode = "wander"
    elif v.mode == "wander":
        xmod, ymod = wander(v)        
    attempt_move(v, m, xmod, ymod,cs,objects)
    
def move_guard(g,player,m,cs,objects):
    if (g.x == player.x and can_see(player.x, player.y, g.y, rotate_list(m,3), objects)
    or (g.y == player.y and can_see(player.y, player.x, g.x, m, objects))):
        g.mode = "chasing"
    if g.mode == "wander":
        xmod, ymod = wander(g)
    elif g.mode == "chasing":        
        xmod, ymod = optupe(pick_direction(g.x, g.y, player.x, player.y))
        g.timer -= 1
        if g.timer == 0:
            g.mode = "wander"
            g.timer = 4
    else:
        xmod,ymod = (0,0)
    if xmod + g.x == player.x and ymod + g.y == player.y:
        news.append("ya got hit")
        player.hp -= 1
    else:
        attempt_move(g, m, xmod, ymod,cs,objects)
    
        
def keyboard_input(inp, player, m, cs, objects):
    ymod = xmod = 0
    if inp == curses.KEY_DOWN:
        ymod = 1
    elif inp == curses.KEY_UP:
        ymod = -1
    elif inp == curses.KEY_LEFT:
        xmod = -1
    elif inp == curses.KEY_RIGHT:        
        xmod = 1
    elif inp == curses.KEY_BACKSPACE:        
        for o in objects:
            if int(distance(player,o)) == 1:
                news.append(o.description)
    elif inp == ord('d'):
        news.append("daytime!")
        day_colors()
    elif inp in map(lambda n: ord(str(n)), range(0, 10)):
        selected_number = inp - 49
        cur_inv = player.inventory.pop(selected_number)
        cur_inv.effect(player, cs)


        
    attempt_move(player, m, xmod, ymod, cs,objects)
    for c in filter(lambda o: o.icon in ["$","8"],objects):
        if player.x == c.x and player.y == c.y:
            player.inventory.append(c)
            news.append("you collected " + c.name)
            objects.remove(c)
    
    vs = filter(lambda c: c.icon == "v", cs)
    for v in vs:
        if player.x == v.x and player.y == v.y:
            news.append("You devour the villager...")
            cs.remove(v)
            body = Object(v.x, v.y, "%", 1, "A dead villager. Eeeewwww.")
            objects.append(body)
            for x in range(2):
                coin = Object(randint(1,MAP_WIDTH),randint(1,MAP_HEIGHT),"$",11, "a coin", "oooh, a coin")
                objects.append(coin)

def wander(c):
    xmod = randint(-1,1)
    ymod = randint(-1,1)
    if randint (0,1) == 1:
        xmod = 0
    else:
        ymod = 0
    return (xmod,ymod)