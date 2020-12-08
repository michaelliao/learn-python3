#!/usr/bin/env python3
# -*- coding: utf-8 -*-

L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']

print('L[0:3] =', L[0:3])
print('L[:3] =', L[:3])
print('L[1:3] =', L[1:3])
print('L[-2:] =', L[-2:])

R = list(range(100))
print('R[:10] =', R[:10])
print('R[-10:] =', R[-10:])
print('R[10:20] =', R[10:20])
print('R[:10:2] =', R[:10:2])
print('R[::5] =', R[::5])


#练习答案
def trim(s):
    a = None
    b = None
    c = 0
    if s == '':
        return ''
    # elif s =='    ':
    #     return ''
    else:
        for i in range(len(s)):
            if s[i] == ' ':
                c = c + 1
                if c == len(s):
                    return ''
        for i in range(len(s)):
            if a != None:
                break
            if s[i] == ' ':
                continue
            else:
                a = i
        for i in range(len(s)):
            if b != None:
                break
            if s[-(i + 1)] == ' ':
                continue
            else:
                b = len(s) - (i + 1) + 1
            if a < b:
                return (s[a:b])
            # elif a == None:
            #     return ''
            else:
                break
            ++i

    
