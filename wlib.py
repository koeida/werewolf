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
        self.original_color = color
        self.color = color
        self.mode = mode
        self.timer = 4
        self.inventory = []
        self.hp = hp
        self.stun_timer = 0
        self.invisibility_timer = 0
        self.target = None

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

def no_wall_between(row, start, end, m):
    inb = between(start, end, m[row])
    
    if 1 or 6 or 8 in inb:
        return False
    else:
        return True
        
        
def no_objects_between(c, t, os, on_x=False, on_y=False):
    startx, endx = ordered(c.x, t.x)
    starty, endy = ordered(c.y, t.y)
    js = list(filter(lambda x: x.icon == "?", os))
    jsx = list(filter(lambda j: j.x > startx and j.x < endx and j.y == c.y, js))
    jsy = list(filter(lambda j: j.y > starty and j.y < endy and j.x == c.x , js))
    if jsx == [] and on_y:
        return True
    if jsy == [] and on_x:
        return True
    return False
# |--------tests----------|  
test_c = Creature(5, 2, "", 0)
test_t = Creature(5, 10, "", 0) 
test_os = []
assert(no_objects_between(test_c, test_t, test_os, True, False) == True)
  
test_c = Creature(5, 2, "", 0)
test_t = Creature(5, 10, "", 0) 
test_os = [Object(5, 5, "?", 0)]
assert(no_objects_between(test_c, test_t, test_os, True, False) == False)

test_c = Creature(5, 2, "", 0)
test_t = Creature(5, 90, "", 0) 
test_os = [Object(8, 5, "?", 0)]
assert(no_objects_between(test_c, test_t, test_os, True, False) == True)
# ________________________|

def can_see(m, c, t ,os):
    def is_visible_(m, n1, n2, f):
    
        open_tiles = [0,2,3,4]
        #open_tiles = filter(lambda tt: tiles[tt][2], tiles)
        visible = lambda l: len(set(l) - set(open_tiles)) == 0

        start, end = ordered(n1, n2)
        tiles_between = [f(n,m) for n in range(start, end + 1)]
        return visible(tiles_between)

    if distance(c,t) > 50:
        return False
    
    if t.invisibility_timer == 0:
        if c.x == t.x:
            return is_visible_(m, c.y, t.y, lambda n,m: m[n][c.x]) and no_objects_between(c,t,os,on_x=True)
        elif c.y == t.y:
            return is_visible_(m, c.x, t.x, lambda n,m: m[c.y][n]) and no_objects_between(c,t,os,on_y=True)
    else:
        return False

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
        if m[ny][nx] in(1, 6, 8) :
            if c.icon != "w":
                xmod, ymod = get_new_mods(xmod, ymod)
            else:
                return
            attempt_move(c, m, xmod, ymod, cs, objects)
            return
        for o in objects:
            if o.x == nx and o.y == ny and o.icon == "?":
                if c.icon != "w":
                    xmod, ymod = get_new_mods(xmod, ymod)
                else:
                    return
                attempt_move(c, m, xmod, ymod, cs, objects)
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

    if can_see(m, v, player,objects):
        v.mode = "fleeing"
        v.timer = 4
    
    if v.mode == "fleeing":
        xmod, ymod = pick_direction(v.x, v.y, player.x, player.y)
        v.timer -= 1
        if v.timer == 0:
            v.mode = "wander"
    elif v.mode == "wander":
        xmod, ymod = wander(v)        
    attempt_move(v, m, xmod, ymod,cs,objects)
    
def move_guard(g,player,m,cs,objects):
    if can_see(m, g, player,objects):
        g.target = (player.x,player.y)

    if g.target is not None:
        xmod, ymod = optupe(pick_direction(g.x, g.y, g.target[0], g.target[1]))
    elif g.target is None:
        xmod, ymod = wander(g)

    if (g.x, g.y) == g.target:
        g.target = None

    if xmod + g.x == player.x and ymod + g.y == player.y:
        news.append("ya got hit")
        player.hp -= 1
    else:
        attempt_move(g, m, xmod, ymod,cs,objects)
    
        
def keyboard_input(inp, player, m, cs, objects):
    ymod = xmod = 0
    movement = 1
    if inp == curses.KEY_DOWN:
        ymod = movement
    elif inp == curses.KEY_UP:
        ymod = -movement
    elif inp == curses.KEY_LEFT:
        xmod = -movement
    elif inp == curses.KEY_RIGHT:        
        xmod = movement
    elif inp == curses.KEY_END:        
        for o in objects:
            if int(distance(player,o)) == 1:
                news.append(o.description)
    elif inp == ord('d'):
        news.append("daytime!")
        day_colors()
    elif inp in map(lambda n: ord(str(n)), range(0, 10)):
        selected_number = inp - 49
        cur_inv = player.inventory.pop(selected_number)
        cur_inv.effect(player, cs,m)


        
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
                guard = Creature(randint(0,MAP_WIDTH), randint(0,MAP_HEIGHT), "g", 5, mode="wander")
                cs.append(guard)
                coin = Object(randint(player.x - 10, player.x + 10),randint(player.y - 10, player.y + 10),"$",11, "a coin", "oooh, a coin")
                objects.append(coin)

def wander(c):
    xmod = randint(-1,1)
    ymod = randint(-1,1)
    if randint (0,1) == 1:
        xmod = 0
    else:
        ymod = 0
    return (xmod,ymod)
