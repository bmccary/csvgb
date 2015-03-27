
from csvu import isnum

def toiorf(x):
    if not isnum(x):
        raise Exception("Not a number: {}".format(x))
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x
        
