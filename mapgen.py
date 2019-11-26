from random import randint, choice
import wlib
import display
from misc import shuffled, w_h

CAM_WIDTH = 50
CAM_HEIGHT = 15

MAP_WIDTH = 1000
MAP_HEIGHT = 1000
MAP_AREA = MAP_WIDTH * MAP_HEIGHT

NUM_POTIONS = int(MAP_AREA / 500)
NUM_JUNKS = int(MAP_AREA * 0.003)

class Zone:
    def __init__ (self, type, percv, percg, percp ,l_func):
        self.type = type
        self.perc_v = percv
        self.perc_g = percg
        self.perc_p = percp
        self.l_func = l_func


def village(m, startx, starty , endx, endy):
    building_zone(m, startx, starty, endx, endy, 100, 4, 4, 10, 10 )
            
def factory(m, startx, starty , endx, endy):
    building_zone(m, startx, starty, endx, endy, 90, 6, 6, 18, 18)
    
def plains(m, startx, starty , endx, endy):
    building_zone(m, startx, starty, endx, endy, 250, 4, 4, 10, 10)
    for x in range(1000):
        m[randint(starty,endy)][randint(startx,endx)] = 9
        
def forest(m, startx, starty , endx, endy):
    for x in range(30000):
        m[randint(starty, endy)][randint(startx, endx)] = 8
 
def mountains(m, startx, starty , endx, endy):
    for y in range(starty,endy):
        for x in range(startx, endx):
            m[y][x] = 6
    
    test_dig = [[6 for x in range(endx - startx)] for y in range(endy - starty)]
    gd = good_dig(test_dig) #dig(300,300, 6, 5, 2, 2, test_dig, 2, 500)
    #dig(30,7, "#", " ", 1, 1, test_dig, 2, 1500)
    #dig(300,300, 6, 5, 2, 10, test_dig, 2, 500)
    stamp(startx,starty,gd,m)
    #for s in range(30000):
    #    m[randint(starty, endy)][randint(startx, endx)] = randint(5, 7)
        
class Digger:
    pass
    
def d_on_map(d, m_hight, m_width): 
    badx = d.x >= m_width + 1 or d.x < 0
    bady = d.y >= m_hight + 1 or d.y < 0
    
    of_map = badx or bady
    if of_map:
        #d.x = sx
        #d.y = sy
        return False
    else:
        return True
        
def ed_check(d, edible,m ,oldx, oldy, m_hight, m_width):
    if d_on_map(d, m_hight, m_width) == False:
        return
    if m[d.y][d.x] != edible:
        d.x,d.y = [oldx, oldy]
    
def dig(sx, sy, edible, eaten, death_rate, s_spawn_rate, m, speed, stop_count):
    m_width = len(m[0]) - 1
    m_hight = len(m) - 1
    d1 = Digger()
    d1.x = sx
    d1.y = sy
    d1.alive = True
    diggers = [d1]
    count = 0
    d1.spawn_rate = s_spawn_rate
    while(len(diggers) > 0):
        count += 1
        if count == stop_count:
            return
        diggers = list(filter(lambda d: d.alive and d_on_map(d, m_hight, m_width), diggers))
        for d in diggers:
            # try:
                # if m[d.y][d.x] == edible:
                    # m[d.y][d.x] = eaten
            # except:
                # print("d.x: %d, d.y: %d" % (d.x, d.y))
                # exit()
            if randint(1, 100) < death_rate:
                d.alive = False
            spawn_chance = randint(1,99)
            if spawn_chance < d.spawn_rate:
                new_digger = Digger()
                bool = (randint(1, 2) == 1)
                new_digger.x = d.x
                new_digger.y = d.y
                new_digger.spawn_rate = s_spawn_rate
                d.spawn_rate = int(d.spawn_rate * 0.95)
                
                if bool:
                    new_digger.x += choice([-1, 1])
                else:
                    new_digger.y += choice([-1, 1])
                new_digger.alive = True            
                diggers.append(new_digger)
            
            oldx, oldy = [d.x, d.y]
            if randint(1, 2) == 1:
                wayx = choice([1,-1])
                for x in range(speed):
                    #on_map(d, m_hight, m_width)
                    if d_on_map(d, m_hight, m_width) == False:
                        break
                    if m[d.y][d.x] == edible:
                        m[d.y][d.x] = eaten
                    d.x  += wayx
                    ed_check(d,edible,m,oldx,oldy, m_hight, m_width)
            else:
                wayy = choice([1,-1])
                for x in range(speed):
                    #on_map(d, m_hight, m_width)
                    if d_on_map(d, m_hight, m_width) == False:
                        break
                    if m[d.y][d.x] == edible:
                        m[d.y][d.x] = eaten
                    d.y  += wayy
                    ed_check(d,edible,m, oldx, oldy, m_hight, m_width)
                    
                    
    
def good_dig(edible=6, eaten=7):
    while(True):
        test_dig = [[edible for x in range(333)] for y in range(333)]
        width, height = w_h(test_dig)
        dig(0, int(height / 25), edible, eaten, 50, 50, test_dig, 2, 1500)
        if edge_touch(test_dig, edible, eaten) >= 2:# and rate_dig(test_dig) <= width * height * 0.5:
            return test_dig
    
        
def rate_dig(dig, edible, eaten):
    rate = 0
    for y in dig:
        for x in y:
            if x == " ":
                rate += 1
    return rate
    
def edge_touch(dig, edible, eaten):
    edges = 0
    e_n = dig[0]
    e_s = dig[-1]
    e_e = []
    e_w = []
    for x in dig:
        e_w.append(x[0])
        e_e.append(x[-1])
    #Keegan's code = "return len(list(filter(lambda e: " " in e, [e_n, e_e, e_s, e_w])))"
    e_spots = [e_n, e_e, e_s, e_w]
    for e in e_spots:
        if eaten in e:
            edges += 1
    return edges
    
        
def building_zone(m, startx, starty , endx, endy, building_divider, minwidth, minhight, maxwidth, maxhight):
    for x in range(int((endx - startx) * (endy - starty) / building_divider)):
            (building_x, building_y, building) = random_building(startx, starty , endx, endy, minwidth, minhight, maxwidth, maxhight)
            stamp_building(building_x, building_y, building, m)


zones = shuffled([
    Zone("factory", 0.0015, 0.0006, 0.002, factory),
    Zone("village", 0.003, 0.0005, 0.001, village),
    Zone("plains", 0.002, 0.0003, 0.001, plains),
    Zone("forest", 0.00015, 0.00015, 0.004, forest),
    Zone("village", 0.003, 0.0005, 0.001, village),
    Zone("mountains", 0.0001, 0.0001, 0.003, mountains),
    Zone("forest", 0.00015, 0.00015, 0.004, forest),
    Zone("lake", 0.0002, 0.0001, 0,village),
    Zone("plains", 0.002, 0.0003, 0.001, plains)])
    
def build_world(zones, m):
    cur_y = 0
    cur_x = 0    
    for z in zones:
        cx = cur_x * 333
        cy = cur_y * 333
        z.l_func(m, cx, cy, cx + 333, cy + 333)
        cur_x += 1
        if cur_x == 3:
            cur_x = 0
            cur_y += 1
    


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

def under_color(c,m):
    tilenum = m[c.y][c.x]
    tile = display.tiles[tilenum]
    u_color = tile[1]
    return u_color

def healing_potion_effect(player,creatures,m):
    player.hp += 2
    wlib.news.append("you drank a healing potion. glug, glug")

def speed_potion_effect(player,creatures,m):
    o = filter(lambda x: x.icon != "w", creatures)
    for x in o:
        x.stun_timer = 3
    wlib.news.append("you drank a speed potion. glug, glug")

def invisibility_potion_effect(player, creatures,m):
    player.invisibility_timer = 8
    wlib.news.append("you drank an invisibility potion. glug, glug")


potions = [ ("a healing potion", healing_potion_effect)
          , ("a speed potion", speed_potion_effect)
          , ("an invisibilaty potion", invisibility_potion_effect)
          ]

def gen_objects(m):
    objectz = []
    for x in range(NUM_POTIONS):
        px = randint(1, MAP_WIDTH - 1)
        py = randint(1, MAP_HEIGHT - 1)
        p, effect = choice(potions)
        potion = wlib.Object(px, py, "8", 13, p, p)
        potion.effect = effect

        objectz.append(potion)
    for x in range(NUM_JUNKS):
        r1 = randint(1,MAP_WIDTH - 1)
        r2 = randint(1,MAP_HEIGHT - 1)
        tile_num = m[r2][r1]
        
        tile = display.tiles[tile_num]
        tile_icon = tile[0]
        
        if if_outdoors(tile_icon):            
            junklist = o_junks            
        else:            
            junklist = i_junks
        junk = wlib.Object(r1,r2, "?",10,choice(junklist), choice(junklist))
        objectz.append(junk)
    return objectz

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

def on_map(x,y,m):
    """Returns True if x,y is within map m"""
    return (x > 0 and x < len(m[0]) and y > 0 and y < len(m))

def random_building(startx, starty, endx, endy, minwidth, minhight, maxhight, maxwidth):
    building_x = randint(startx, endx)
    building_y = randint(starty, endy)
    building_width = randint(minwidth,maxwidth)
    building_height = randint(minhight,maxhight)
    building = make_building(building_width, building_height)
    return (building_x, building_y, building)

#m = good_dig()
#print("DONE!")
#dig(300,300, 6, 5, 2, 10, test_dig, 2, 50)#count = 0
#for row in m:
#    print("".join(row)) 

#stamp(0,0,test_dig,test_dig)
#exit()