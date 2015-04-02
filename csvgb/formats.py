
from csvgb import isnum, isna, all_g, isexempt, K_EXEMPT

def custom(x):
    if isna(x):
        return x
    if isexempt(x):
        return K_EXEMPT
    if not isnum(x):
        raise Exception("Not a number: {}".format(x))
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x

for k in all_g():
    globals()[k] = custom

