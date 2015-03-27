
from pprint import pformat
import traceback
import functools
from copy import copy
from csvu import isnum, isstr, isna as isna_, K_NAs as K_NAs_
import csvu






K_MISSED = 'Missed'
K_MISSED_UPPER = K_MISSED.upper()

K_EXEMPT = 'Exempt'
K_EXEMPT_UPPER = K_EXEMPT.upper()

K_RANSOMED = 'Ransomed'
K_RANSOMED_UPPER = K_RANSOMED.upper()

K_NAs = copy(K_NAs_)

K_NAs.extend([K_MISSED, K_RANSOMED])

def isexempt(x):
    if isstr(x):
        return x.strip().upper() == K_EXEMPT_UPPER
    return False

def ismissed(x):
    if isstr(x):
        return x.strip().upper() == K_MISSED_UPPER
    return False

def isransomed(x):
    if isstr(x):
        return x.strip().upper() == K_RANSOMED_UPPER
    return False






isna = functools.partial(isna_, K=K_NAs)

def _fix(f):
    def g(x):
        if isexempt(x):
            return K_EXEMPT
        if ismissed(x):
            return K_MISSED
        if isna(x):
            if x in ['', 'NA', None, []]:
                return x
            if x == 'NONE':
                return 'None'
            raise Exception("Unknown NA: {}".format(x))
        if isransomed(x):
            return K_RANSOMED
        return f(x, isna=isna)
    return g

CSVU_IMPORTS_ISNA = [
        'toint',
        'tofloat',
        'tonnint',
        'tonnfloat',
        'tozero',
        'sum0',
        'mean0',
        'drop0',
        'max0',
        'min0',
        'equal0',
        'inner0',
    ]

for i in CSVU_IMPORTS_ISNA:
    f = getattr(csvu, i, None)
    g = _fix(f)
    globals()[i] = g

del i
del f
del g

