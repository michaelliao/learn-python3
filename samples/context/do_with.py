#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from contextlib import contextmanager

@contextmanager
def log(name):
    print('[%s] start...' % name)
    yield
    print('[%s] end.' % name)

with log('DEBUG'):
    print('Hello, world!')
    print('Hello, Python!')
