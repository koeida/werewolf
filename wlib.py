from random import randint, choice
import curses
from math import sqrt

MAP_WIDTH = 100
MAP_HEIGHT = 30

news = []
i_junks = [ "a shelf of ancient tomes,oh how old"
          , "a comfy sofa, should I sit down?"
          , "a desk. very desky."
          , "a pile of rubble. what happened here?"
          , "dirty laundry. oh, it reeks"
          ]

o_junks = [ "a pile of rubble. what happened here?"
          , "a hay bale. where's the needle?"
          , "a campfire.  nice and toasty!"
          , "a mail box. stuffed with bills:("
          , "a mail box. stuffed with love letters:)"
          ]

tiles = {0: (".",0),
         1: ("#",2),
         2: ("\"",3),
         3: ("_",1)}

def gen_objects(m):
    objects = []
    for x in range(5):
        r1 = randint(1,MAP_WIDTH)
        r2 = randint(1,MAP_HEIGHT)
        tile_num = m[r2][r1]
        tile = tiles[tile_num]        
        tile_icon = tile[0]
        
        if if_outdoors(tile_icon):            
            junklist = o_junks            
        else:            
            junklist = i_junks
        junk = Object(r1,r2, "?", choice(junklist))
        objects.append(junk)
    return objects

def distance(c1,c2):
    a = c1.x - c2.x      
    b = c1.y - c2.y
    c = a**2 + b**2
    
    return sqrt(c)

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
    def __init__(self, x, y, icon, description = ""):
        self.icon = icon
        self.x = x
        self.y = y
        self.description = description
        

def can_see(row, start, end, m):   
    inb = between(start,end,m[row])
    if 1 in inb:
        return False
    else:
        return True

def can_see_old(c, t, m):
    inb = m[c.y][c.x:t.x]
    if 1 in inb:
        return False
    else:
        return True
    #if in the list of tiles between c and t there is a wall
        # then False
    #else:
        #True
        

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
    
def rotate_list(l, n = 1):
    newlist = l
    for x in range(n):
        newlist = list(zip(*newlist[::-1]))
    return newlist

def between(i1,i2,l):
    """between(1,3,l) == between(3,1,l)"""
    if i1 < i2:
        return l[i1:i2]
    else:
        return l[i2:i1]
    
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
    
    if (v.x == player.x and can_see(player.x, player.y, v.y, rotate_list(m,3))
    or (v.y == player.y and can_see(player.y, player.x, v.x, m))):
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
            body = Object(v.x, v.y, "%", "A dead villager. Eeeewwww.")
            objects.append(body)
            for x in range(2):
                coin = Object(randint(1,MAP_WIDTH),randint(1,MAP_HEIGHT),"$","oooh, a coin")
                objects.append(coin) 
            
                   
def display_news(screen, news):
    top_news = news[-5:]
    top_news.reverse()
    cn = 0
    for n in top_news:
        screen.addstr(MAP_HEIGHT + cn, 0, " " * MAP_WIDTH, curses.color_pair(5 + cn)), 
        screen.addstr(MAP_HEIGHT + cn, 0, n, curses.color_pair(5 + cn))
        cn += 1


def init_colors():
    curses.init_color(2, 600, 400, 255)
    curses.init_color(3, 0, 1000, 0)
    curses.init_color(4, 800, 600, 455)
    curses.init_color(5, 1000, 1000, 1000)
    
    # Shades of grey for news
    curses.init_color(6, 800, 800, 800)
    curses.init_color(7, 600, 600, 600)
    curses.init_color(8, 400, 400, 400)
    curses.init_color(9, 300, 300, 300)
    
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)
    
    # News fadeout
    curses.init_pair(6, 6, curses.COLOR_BLACK)
    curses.init_pair(7, 7, curses.COLOR_BLACK)
    curses.init_pair(8, 8, curses.COLOR_BLACK)
    curses.init_pair(9, 9, curses.COLOR_BLACK)
    

def on_map(x,y,m):
    """Returns True if x,y is within map m"""
    return (x > 0 and x < len(m[0]) and y > 0 and y < len(m))

def stamp(x,y,s,m):
    """Stamps s onto m at coordinates x,y"""
    for sy in range(len(s)):
        for sx in range(len(s[0])):
            if on_map(x + sx, y + sy, m):
                m[y + sy][x + sx] = s[sy][sx]
                
def stamp_building(x,y,s,m):
    """Stamps building s onto m at coordinates x,y"""
    for sy in range(len(s)):
        for sx in range(len(s[0])):
            if on_map(x + sx, y + sy, m):                
                new_tile = s[sy][sx]
                if m[y + sy][x + sx] == 0:
                    m[y + sy][x + sx] = 0
                else:
                    m[y + sy][x + sx] = new_tile
            

def make_list_of_1s(n):
    l = []
    for x in range(n):
       l.append(1)
    return l

def make_middle(n):
    l = [1]
    for x in range(n - 2):
        l.append(0)
    l.append(1)
    return l

def is_corner(x, y, w, h):
    if x == 0 and y == h:
        return True
    elif x == 0 and y == 0:
        return True
    elif x == w and y == 0:
        return True
    elif x == w and y == h:
        return True
    return False
    
def make_building(w,h):
    """Returns a list of lists of tile numbers"""
    results = []
    # Top row is always all 1s: 4 --> [1,1,1,1]
    top_row = make_list_of_1s(w)
    results.append(top_row)
    for x in range(h - 2):
        middle_row = make_middle(w)
        results.append(middle_row)
    bottom_row = make_list_of_1s(w)
    results.append(bottom_row)
    # Middle rows, first tile is 1
    for row in range(h):
        for column in range(w):
            if results[row][column] == 1 and randint(1,20) == 1 and not is_corner(column,row,w,h):
                results[row][column] = 3
                return results
    return results

    
def if_outdoors(tile):
    if tile == "\"":
        return True
    return False
#for row in make_building(randint(4,15),randint(4,15)):
#    print(row)