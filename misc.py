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

    
