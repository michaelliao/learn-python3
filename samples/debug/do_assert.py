#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n

def debug_msg(msg):
    assert len(msg) > 0
    print(msg)

def main():
    foo('0')
    debug_msg('debug')
    debug_msg('')

main()
