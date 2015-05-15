#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools

natuals = itertools.count(1)
for n in natuals:
    print(n)
    if n >= 100:
        break

cs = itertools.cycle('ABC')
t = 10
for c in cs:
    print(c)
    t = t - 1
    if t == 0:
        break
