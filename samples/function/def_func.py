#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

#Viene definita la funzione valore assoluto
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

#Muove un punto nel piano cartesiano 2D
#dove step è il modulo dello spostamento
#e angle è la sua direzione in radianti
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny

n = my_abs(-20)
print(n)

x, y = move(100, 100, 60, math.pi / 6)
print(x, y)

# TypeError: bad operand type:
my_abs('123')
