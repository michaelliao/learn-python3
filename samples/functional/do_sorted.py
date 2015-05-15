#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter

L = ['bob', 'about', 'Zoo', 'Credit']

print(sorted(L))
print(sorted(L, key=str.lower))

students = [
    ('Adam', 90),
    ('Tim', 60),
    ('Lisa', 80),
    ('Bart', 60)
]

print(sorted(students, key=itemgetter(1)))

def student_to_key(t):
    return '%+02d%s' % (100-t[1], t[0])

print(sorted(students, key=student_to_key))
