from random import randint, shuffle
from copy import deepcopy

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
    
def optupe(t):
    v1, v2 = t
    v1 *= -1
    v2 *= -1
    return (v1,v2)

def ordered(x,y):
    o1 = x if x < y else y
    o2 = x if x > y else y
    return (o1, o2)
    
def get_new_mods(xmod, ymod):
    if ymod == 0:
        return (0, randint(-1, 1))
    elif xmod == 0:
        return(randint(-1, 1), 0)
    else:
        assert(False)
        
def shuffled(l):
    l2 = deepcopy(l)
    shuffle(l2)
    return l2

def w_h(m):
    return (len(m[0]), len(m))

