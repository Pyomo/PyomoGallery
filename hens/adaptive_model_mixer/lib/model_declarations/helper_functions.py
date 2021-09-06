# Authors: Miten Mistry and Ruth Misener
#         Department of Computing, Imperial College London

from math import log

def two_point_generator(points, bounds):
    lower, upper = bounds
    ret_set = []
    for pa, pb in points:
        x = lower*pa + upper*pb
        ret_set.append(x)
    return ret_set

def three_point_generator(points, bounds):
    lower, upper = bounds
    ax, ay = lower, lower
    bx, by = upper, upper
    cx, cy = upper, lower
    ret_set = []
    for pa, pb, pc in points:
        x0 = ax*pa + bx*pb + cx*pc
        y0 = ay*pa + by*pb + cy*pc
        ret_set.append((x0,y0))
        if not x0 == y0:
            ret_set.append((y0,x0))
    return ret_set

def lmtd_inv(x, y):
    return log(x/y)/(x-y) if (x != y) else 1/x

def lmtd_inverse_gradient_calculator(x0, y0):
    if x0 == y0:
        return (-1/(2*pow(x0,2)),-1/(2*pow(y0,2)))
    else:
        w = x0/y0
        scale = 1/(pow((x0-y0),2))
        return (scale*(1-(1/w)-log(w)), scale*(1+log(w)-w))
