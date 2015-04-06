
from string import zfill
from functools import partial
from csvgb import isnum, isint, isna, all_g, isexempt, K_EXEMPT

def default(x):
    if isna(x):
        return x
    if isexempt(x):
        return K_EXEMPT
    if not isnum(x):
        raise Exception("Not a number: {}".format(x))
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x

def lexical_int(x, width=2):
    if isint(x):
        return zfill(str(int(x)), width)
    return x
lexical_int2 = partial(lexical_int, width=2)
lexical_int3 = partial(lexical_int, width=3)

def lexical_float(x):
    if isnum(x):
        return zfill('{:.3f}'.format(x), 7)
    return x

for k in all_g():
    globals()[k] = default

