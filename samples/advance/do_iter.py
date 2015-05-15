#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Iterable
print('iterable? [1, 2, 3]:', isinstance([1, 2, 3], Iterable))
print('iterable? \'abc\':', isinstance('abc', Iterable))
print('iterable? 123:', isinstance(123, Iterable))

# iter list:
print('iter [1, 2, 3, 4, 5]')
for x in [1, 2, 3, 4, 5]:
    print(x)

d = {'a': 1, 'b': 2, 'c': 3}

# iter each key:
print('iter key:', d)
for k in d.keys():
    print('key:', k)

# iter each value:
print('iter value:', d)
for v in d.values():
    print('value:', v)

# iter both key and value:
print('iter item:', d)
for k, v in d.items():
    print('item:', k, v)

# iter list with index:
print('iter enumerate([\'A\', \'B\', \'C\']')
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)

# iter complex list:
print('iter [(1, 1), (2, 4), (3, 9)]:')
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)
