
from csvgb import tonnfloat, all_g

for k in all_g():
    globals()[k] = tonnfloat

