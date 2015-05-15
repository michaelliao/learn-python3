#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

@contextmanager
def closing(fname):
    f = None
    try:
        f = open(fname, 'r')
        yield f
    finally:
        if f:
            f.close()

with closing('test.txt') as f:
    print(f.read())
