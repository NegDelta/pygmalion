# Sign fn
def sgn(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return None

# Interpolate between x0 (for k=0) & x1 (for k=1)
def ipol(x0, x1, k):
    return x0 + (x1-x0) * k

# Get factor from interpolated value
def rev_ipol(x0, x1, x):
    try:
        return (x - x0)/(x1 - x0)
    except ZeroDivisionError:
        return 0
        
# React to movement key being pressed
def diradd(p1,p2):
    if p1[0] == 0:
        p1[0] = p2[0]
    if p1[1] == 0:
        p1[1] = p2[1]
    return p1

# React to movement key being released
def dirsub(p1,p2):
    if p1[0]*p2[0] > 0: # signs match and non-zero
        p1[0] = 0
    if p1[1]*p2[1] > 0:
        p1[1] = 0
    return p1

# Return vector of same direction but of given length
def unitize(v, length=1):
    acc = 0
    for i in v:
        acc += i**2
    veclen = acc ** 0.5
    if veclen == 0:
        return v
    va = []
    for i in v:
        va += [i * length / veclen]
    return va

# Return coordinate offset from block that point is in
# and border about to be hit with given velocity
def getborder(dirv):
    return int(dirv > 0)
