
from functools import partial
from csvgb import tonnfloat, toint, all_g, equal0, isna

for k in all_g():
    globals()[k] = tonnfloat

