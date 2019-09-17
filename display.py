import curses
from mapgen import MAP_HEIGHT, MAP_WIDTH

tiles = {0: (".",0),
         1: ("#",2),
         2: ("\"",3),
         3: ("_",1),
         4: ("~",12)}

def display_news(screen, news):
    top_news = news[-5:]
    top_news.reverse()
    cn = 0
    for n in top_news:
        screen.addstr(MAP_HEIGHT + cn, 0, " " * MAP_WIDTH, curses.color_pair(5 + cn)), 
        screen.addstr(MAP_HEIGHT + cn, 0, n, curses.color_pair(5 + cn))
        cn += 1
        
def limit(foo,limit, bottom=0):
    if foo <= limit and foo >= bottom:
        return foo
    elif foo <= limit and foo <= bottom:
        return bottom
    else:
        return limit
assert(limit(10,5) == 5)
assert(limit(10,30) == 10)
assert(limit(-10,10) == 0)

def winit_color(cn, r, g, b):
    nr = limit(r,1000)
    ng = limit(g,1000)
    nb = limit(b,1000)
    curses.init_color(cn, nr, ng, nb)
    
def night_colors():
    winit_color(2, 450, 300, 100)
    winit_color(3, 0, 600, 100)
    winit_color(4, 600, 400, 255)
    winit_color(5, 800, 800, 800)
    winit_color(13, 600, 180, 670)
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK )
    curses.init_pair(3, 3, curses.COLOR_BLACK ) 
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)
    curses.init_pair(13, 13, curses.COLOR_BLACK)

def day_colors():
    winit_color(2, 600, 400, 255)
    winit_color(3, 0, 1000, 0)
    winit_color(4, 800, 600, 455)
    winit_color(5, 1000, 1000, 1000)

def init_colors(mod=0):
    night_colors()
    
    # Shades of grey for news
    winit_color(6, 800, 800, 800)
    winit_color(7, 600, 600, 600)
    winit_color(8, 400, 400, 400)
    winit_color(9, 300, 300, 300)
    
    winit_color(10, 800, 600, 300)    
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 2, curses.COLOR_BLACK) #walls, brown on black
    curses.init_pair(3, 3, curses.COLOR_BLACK) 
    curses.init_pair(4, 4, curses.COLOR_BLACK)
    curses.init_pair(5, 5, curses.COLOR_BLACK)
    
    # News fadeout
    curses.init_pair(6, 6, curses.COLOR_BLACK)
    curses.init_pair(7, 7, curses.COLOR_BLACK)
    curses.init_pair(8, 8, curses.COLOR_BLACK)
    curses.init_pair(9, 9, curses.COLOR_BLACK)
    
    curses.init_pair(10, 10, curses.COLOR_BLACK)
    curses.init_pair(11, 11, curses.COLOR_BLACK)
    curses.init_pair(12, curses.COLOR_BLUE, curses.COLOR_BLACK)
    
def draw_map(screen, tiles, m):
    for row in range(len(m)):
        for column in range(len(m[0])):
            cur_tile_num = m[row][column]
            cur_tile = tiles[cur_tile_num][0]
            screen.addstr(row, column, cur_tile, curses.color_pair(tiles[cur_tile_num][1]))

def display_hp(screen, hp):
    s = "+" * hp 
    screen.addstr(14, MAP_WIDTH + 1, "health: " + s, curses.color_pair(1))
    
def display_inv(screen, inventory):
    screen.addstr(0, MAP_WIDTH + 1, "Inventory:")
    ci = 1
    for i in inventory:
        screen.addstr(ci, MAP_WIDTH + 1, str(ci) + ") ", curses.color_pair(0))
        screen.addstr(ci, MAP_WIDTH + 4, i.icon, curses.color_pair(i.color))
        screen.addstr(ci, MAP_WIDTH + 5, ": " + i.name, curses.color_pair(0))
        ci += 1