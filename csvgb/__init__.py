
from pprint import pformat
import traceback
from functools import partial
from copy import copy
from csvu import *
import csvu
from itertools import chain


K_MISSED = 'Missed'
K_MISSED_UPPER = K_MISSED.upper()

K_EXEMPT = 'Exempt'
K_EXEMPT_UPPER = K_EXEMPT.upper()

K_RANSOMED = 'Ransomed'
K_RANSOMED_UPPER = K_RANSOMED.upper()

K_NEEDS_GRADING = 'Needs Grading'
K_NEEDS_GRADING_UPPER = K_NEEDS_GRADING.upper()

K_NAs = copy(csvu.K_NAs)

K_NAs.extend([K_EXEMPT_UPPER, K_MISSED_UPPER, K_RANSOMED_UPPER, K_NEEDS_GRADING_UPPER])

isna = partial(csvu.isna, K=K_NAs)

def isexempt(x):
    if isstr(x):
        return x.strip().upper() == K_EXEMPT_UPPER
    return False

def ismissed(x):
    if isstr(x):
        return x.strip().upper() == K_MISSED_UPPER
    return False

def isneedsgrading(x):
    if isstr(x):
        return x.strip().upper() == K_NEEDS_GRADING_UPPER
    return False

def isransomed(x):
    if isstr(x):
        return x.strip().upper() == K_RANSOMED_UPPER
    return False

def isint(x):
    if isinstance(x, int):
        return True
    if isinstance(x, float) and x.is_integer():
        return True
    return False

def _fix(f):
    def g(x):
        if isexempt(x):
            return K_EXEMPT
        if ismissed(x):
            return K_MISSED
        if isneedsgrading(x):
            return K_NEEDS_GRADING
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

CSVU_IMPORTS_TO_FIX = [
        'toint',
        'tofloat',
        'tonnint',
        'tonnfloat',
        'tozero',
        'sum0',
        'mean0',
        'max0',
        'min0',
        'drop0',
        'equal0',
        'inner0',
    ]

for i in CSVU_IMPORTS_TO_FIX:
    f = getattr(csvu, i, None)
    g = partial(f, isna=isna)
    globals()[i] = g

K_EXAM_N     = 4
K_HOMEWORK_N = 13
K_QUIZ_N     = 13
K_THQ_N      = 13

K_EXAM_ALL     = ['exam_{:02d}'.format    (m+1) for m in xrange(K_EXAM_N)]
K_HOMEWORK_ALL = ['homework_{:02d}'.format(m+1) for m in xrange(K_HOMEWORK_N)]
K_QUIZ_ALL     = ['quiz_{:02d}'.format    (m+1) for m in xrange(K_QUIZ_N)]
K_THQ_ALL      = ['thq_{:02d}'.format     (m+1) for m in xrange(K_THQ_N)]

def exam_g():
    s = 'exam'
    for m in range(K_EXAM_N):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in range(12):
            yield '{}_{:02d}'.format(s_m, n + 1)
        for n in ['max', 'min', 'penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)

def homework_g():
    s = 'homework'
    for m in range(K_HOMEWORK_N):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in ['penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)
    for m in ['grade', 'grade_min', 'grade_max', 'misses_pct', 'misses_count',]:
        yield '{}_{}'.format(s, m)

def quiz_g():
    s = 'quiz'
    for m in range(K_QUIZ_N):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in range(3):
            yield '{}_{:02d}'.format(s_m, n + 1)
        for n in ['penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)
    for m in ['grade', 'grade_min', 'grade_max', 'misses_pct', 'misses_count',]:
        yield '{}_{}'.format(s, m)

def thq_g():
    s = 'thq'
    for m in range(K_THQ_N):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in range(3):
            yield '{}_q{}'.format(s_m, n + 1)
        for n in ['penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)
    for m in ['grade', 'grade_min', 'grade_max', 'misses_pct', 'misses_count',]:
        yield '{}_{}'.format(s, m)

def course_g():
    s = 'course'
    for m in ['misses', 'misses_count', 'misses_pct', 'participation']:
        s_m = '{}_{}'.format(s, m)
        yield s_m
    s = 'course_grade'
    yield s
    for m in ['max', 'min', 'midterm', 'penultimate']:
        s_m = '{}_{}'.format(s, m)
        yield s_m

def all_g():
    return chain(course_g(), exam_g(), homework_g(), quiz_g(), thq_g())


