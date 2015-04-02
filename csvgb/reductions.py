
from itertools import izip

from csvgb import (
        isna, 
        isnum, 
        isexempt,
        ismissed,
        isransomed,
        sum0,
        drop0,
        mean0,
        K_RANSOMED,
        K_MISSED,
        K_EXAM_N,
        K_HOMEWORK_N,
        K_QUIZ_N,
        K_THQ_N,
    )

def _exam_XX_f(m):
    s_m   = 'exam_{:02d}'.format(m)
    s_m_o = '{}_override'.format(s_m)
    s_m_p = '{}_penalty'.format(s_m)
    s_m_r = '{}_ransom'.format(s_m)
    s_m_n = ['{}_{:02d}'.format(s_m, n + 1) for n in xrange(12)]
    def f(row, K):
        r = row.get(s_m_r)
        if not isna(r):
            return K_RANSOMED
        o = row.get(s_m_o)
        if not isna(o):
            return o
        v = sum0([row.get(k) for k in s_m_n])
        if isna(v):
            if s_m in K:
                return K_MISSED
            return v
        p = row.get(s_m_p)
        if isnum(p):
            v = max(v - p, 0)
        return v
    return s_m, f

def _quiz_XX_f(m):
    s_m   = 'quiz_{:02d}'.format(m)
    s_m_o = '{}_override'.format(s_m)
    s_m_p = '{}_penalty'.format(s_m)
    s_m_r = '{}_ransom'.format(s_m)
    s_m_n = ['{}_{:02d}'.format(s_m, n + 1) for n in xrange(3)]
    def f(row, K):
        r = row.get(s_m_r)
        if not isna(r):
            return K_RANSOMED
        o = row.get(s_m_o)
        if not isna(o):
            return o
        v = sum0([row[k] for k in s_m_n])
        if isna(v):
            if s_m in K:
                return K_MISSED
            return v
        p = row.get(s_m_p)
        if isnum(p):
            v = max(v - p, 0)
        return v
    return s_m, f

def _thq_XX_f(m):
    s_m   = 'thq_{:02d}'.format(m)
    s_m_o = '{}_override'.format(s_m)
    s_m_p = '{}_penalty'.format(s_m)
    s_m_r = '{}_ransom'.format(s_m)
    s_m_n = ['{}_q{}'.format(s_m, n + 1) for n in xrange(3)]
    def f(row, K):
        r = row.get(s_m_r)
        if not isna(r):
            return K_RANSOMED
        o = row.get(s_m_o)
        if not isna(o):
            return o
        v = sum0([row[k] for k in s_m_n])
        if isna(v):
            if s_m in K:
                return K_MISSED
            return v
        p = row.get(s_m_p)
        if isnum(p):
            v = max(v - p, 0)
        return v
    return s_m, f

for m in xrange(K_EXAM_N):
    s_m, f = _exam_XX_f(m + 1)
    globals()[s_m] = f

for m in xrange(K_QUIZ_N):
    s_m, f = _quiz_XX_f(m + 1)
    globals()[s_m] = f

for m in xrange(K_THQ_N):
    s_m, f = _thq_XX_f(m + 1)
    globals()[s_m] = f

def X_all(row, K): return [row[k] for k in K if not isexempt(row[k])]

def homework_grade(row, K, D): return mean0(drop0(X_all(row, K), D))

def quiz_grade(row, K, D): 
    m = mean0(drop0(X_all(row, K), D))
    if isna(m):
        return m
    return m/30.0*100.0

def thq_grade(row, K, D): 
    m = mean0(drop0(X_all(row, K), D))
    if isna(m):
        return m
    return m/30.0*100.0

def X_misses_g(row, K): return (k for k in K if ismissed(row[k]))

def X_misses_count(row, K): return sum(1 for x in X_misses_g(row, K))

def X_misses_percent(row, K, D):
    N = len(_all(row, k))
    if N <= D:
        return None
    M = max(X_misses_count(row, K) - D, 0)
    return float(M)/N*100.0

def X_ransom_g(row, K):
    for k in K:
        s = '{}_ransom'.format(k)
        if isransomed(row.get(s)):
            yield k

def X_ransom_count(row, K): return sum(1 for x in X_ransom_g(row, K))

LETTER         = [ 'F',          'D',                 'C',                 'B',                 'A', ]
LETTER_CUTS    = [             60.00,               70.00,               80.00,               90.00, ]
LETTER_PM      = [ 'F',  'D-',   'D',  'D+',  'C-',   'C',  'C+',  'B-',   'B',  'B+',  'A-',   'A',  'A+', ]
LETTER_CUTS_PM = [      60.00, 63.33, 66.66, 70.00, 73.33, 76.66, 80.00, 83.33, 86.66, 90.00, 93.33, 96.66, ]

def letterize(grade, cuts=LETTER_CUTS_PM):

    if type(cuts) != list:
        raise Exception("Bad cuts: " + str(cuts))

    L = None

    if len(cuts) == len(LETTER) - 1:
        L = LETTER
    elif len(cuts) == len(LETTER_PM) - 1:
        L = LETTER_PM
    else:
        raise Exception("Bad cuts: " + str(cuts))

    for c, l in izip(cuts, L):
        if grade < c:
            return l

    return L[-1]

_gpa_d = {
    "A+": 4.000,
    "A" : 4.000,
    "A-": 3.670,
    "B+": 3.330,
    "B" : 3.000,
    "B-": 2.670,
    "C+": 2.330,
    "C" : 2.000,
    "C-": 1.670,
    "D+": 1.330,
    "D" : 1.000,
    "D-": 0.670,
    "F" : 0.000,
    "NF": 0.000,
            }

def gpaize(grade):
    v = _gpa_d.get(grade)
    if v is None:
        raise Exception("Unknown grade: {}".format(grade))
    return v

def donothing(row):
    return None

