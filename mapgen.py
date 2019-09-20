from random import randint, choice
import wlib
import display

MAP_WIDTH = 100
MAP_HEIGHT = 30

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


def healing_potion_effect(player,creatures):
    player.hp += 2
    wlib.news.append("you drank a healing potion. glug, glug")

def speed_potion_effect(player,creatures):
    o = filter(lambda x: x.icon != "w", creatures)
    for x in o:
        x.stun_timer = 3

def invisibility_potion_effect(player, creatures):
    pass


potions = [ ("a healing potion", healing_potion_effect)
          , ("a speed potion", speed_potion_effect)
          , ("an invisibilaty potion", invisibility_potion_effect)
          ]

def gen_objects(m):
    objects = []
    for x in range(50):
        px = randint(1, MAP_WIDTH - 1)
        py = randint(1, MAP_HEIGHT - 1)
        p, effect = choice(potions)
        potion = wlib.Object(px, py, "8", 13, p, p)
        potion.effect = effect

        objects.append(potion)
    for x in range(20):
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
        objects.append(junk)
    return objects

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

def random_building():
    building_x = randint(2,MAP_WIDTH)
    building_y = randint(2,MAP_HEIGHT)
    building_width = randint(4,15)
    building_height = randint(4,15)
    building = make_building(building_width, building_height)
    return (building_x, building_y, building)

