
from csvgb import (
        isna, 
        isnum, 
        tonnfloat, 
        tozero as tozero_
        sum0,
        K_MISSED,
        K_RANSOMED,
    )

def init_quiz():
    for m in range(12):
        s_m, f = _quiz_XX_f(m)
        if not globals().has_key(s_m):
            globals()[s_m] = f

def init():
    init_quiz()

def _exam_XX_f(m):
    s_m   = 'exam_{:02d}'.format(m)
    s_m_o = '{}_override'.format(s_m)
    s_m_p = '{}_penalty'.format(s_m)
    s_m_n = ['{}_{:02d}'.format(s_m, n + 1) for n in range(10)]
    def f(row):
        o = row[s_m_o]
        if isna(o):
            v = sum0([row[k] for k in s_m_n])
            p = row[s_m_p]
            if isnum(p):
                v -= p
            return v
        return o
    return s_m, f

def _quiz_XX_f(m):
    s_m   = 'quiz_{:02d}'.format(m)
    s_m_o = '{}_override'.format(s_m)
    s_m_p = '{}_penalty'.format(s_m)
    s_m_n = ['{}_{:02d}'.format(s_m, n + 1) for n in range(3)]
    def f(row):
        o = row[s_m_o]
        if isna(o):
            v = sum0([row[k] for k in s_m_n])
            p = row[s_m_p]
            if isnum(p):
                v -= p
            return v
        return o
    return s_m, f

def _thq_XX_f(m):
    s_m   = 'thq_{:02d}'.format(m)
    s_m_o = '{}_override'.format(s_m)
    s_m_p = '{}_penalty'.format(s_m)
    s_m_n = ['{}_q{}'.format(s_m, n + 1) for n in range(3)]
    def f(row):
        o = row[s_m_o]
        if isna(o):
            v = sum0([row[k] for k in s_m_n])
            p = row[s_m_p]
            if isnum(p):
                v -= p
            return v
        return o
    return s_m, f

