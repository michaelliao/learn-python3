#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

# Function using def
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

# Lambda function equivalent
lambda_abs = lambda x: x if x >= 0 else -x

# Function using def
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny

# Lambda function equivalent
lambda_move = lambda x, y, step, angle=0: (x + step * math.cos(angle), y - step * math.sin(angle))

# Examples
n_def = my_abs(-20)
n_lambda = lambda_abs(-20)
print(n_def, n_lambda)

x_def, y_def = move(100, 100, 60, math.pi / 6)
x_lambda, y_lambda = lambda_move(100, 100, 60, math.pi / 6)
print(x_def, y_def, x_lambda, y_lambda)


my_abs('123')
