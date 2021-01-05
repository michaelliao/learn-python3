#!/usr/bin/python
# -*- coding: utf-8 -*-
def trim(s):
    start = 0
    end = 0
    pos = 0
#find first non-space from left
    while(pos <len(s)):
        if s[pos] == ' ':
            pos += 1
            continue
        elif s[pos] != ' ':
            start = pos
            break
    pos = len(s) - 1
#find first non-space from right
    while(pos >=0):
        if s[pos] == ' ':
            pos -= 1
            continue
        elif s[pos] != ' ':
            end = pos + 1
            break
#return slice
    return s[start:end]
