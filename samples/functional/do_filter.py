#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_odd(n):
    return n % 2 != 0//maybe this definition is more robust.

L = range(100)

print(list(filter(is_odd, L)))

def not_empty(s):
    return s and s.strip()

print(list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))
