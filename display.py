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
    
    curses.init_color(10, 800, 600, 300) #junk color
    
    
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
