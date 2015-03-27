
from itertools import chain, product

from csvgb import (
        isna, 
        toint, 
        tonnint, 
        tofloat, 
        tonnfloat as tonnfloat_, 
        isexempt,   K_EXEMPT,
        ismissed,   K_MISSED,
        isransomed, K_RANSOMED,
    )

def init_quiz():
    s = 'quiz'
    for m in range(14):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in range(3):
            yield '{}_{:02d}'.format(s_m, n + 1)
        for n in ['penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)
    for m in ['grade', 'grade_min', 'grade_max', 'misses_pct', 'misses_count',]:
        yield '{}_{}'.format(s, m)

def init_thq():
    s = 'thq'
    for m in range(12):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in range(3):
            yield '{}_q{}'.format(s_m, n + 1)
        for n in ['penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)
    for m in ['grade', 'grade_min', 'grade_max', 'misses_pct', 'misses_count',]:
        yield '{}_{}'.format(s, m)

def init_homework():
    s = 'homework'
    for m in range(12):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in ['penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)
    for m in ['grade', 'grade_min', 'grade_max', 'misses_pct', 'misses_count',]:
        yield '{}_{}'.format(s, m)

def init_exam():
    s = 'exam'
    for m in range(4):
        s_m = '{}_{:02d}'.format(s, m + 1)
        yield s_m
        for n in range(12):
            yield '{}_{:02d}'.format(s_m, n + 1)
        for n in ['max', 'min', 'penalty', 'override',]:
            yield '{}_{}'.format(s_m, n)

def init_course():
    s = 'course'
    for m in ['misses', 'misses_count', 'misses_pct', 'participation']:
        s_m = '{}_{}'.format(s, m)
        yield s_m

    s = 'course_grade'
    yield s
    for m in ['max', 'min', 'midterm', 'penultimate']:
        s_m = '{}_{}'.format(s, m)
        yield s_m

def init():

    for k in chain(init_quiz(), init_thq(), init_exam(), init_homework(), init_course()):
        globals()[k] = tonnfloat

