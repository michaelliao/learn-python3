#!/usr/bin/env python3
# -*- coding: utf-8 -*-

classmates = ['Michael', 'Bob', 'Tracy']
print('classmates =', classmates)
print('len(classmates) =', len(classmates))
print('classmates[0] =', classmates[0])
print('classmates[1] =', classmates[1])
print('classmates[2] =', classmates[2])
print('classmates[-1] =', classmates[-1])
classmates.pop()
print('classmates =', classmates)

#append values to list
classmates.append('Pam')
print(classmates)

#insert at particular index
classmates.insert(1,'Jim')
print(classmates)

#reverse the list
classmates.reverse()
print(classmates)
