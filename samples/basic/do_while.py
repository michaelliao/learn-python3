#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 计算1+2+3+...+100:
sum = 0
n = 1
while n <= 100:
    sum = sum + n
    n = n + 1
print(sum)

# 计算1x2x3x...x100:
acc = 1
n = 1
while n <= 100:
    acc = acc * n
    n = n + 1
print(acc)
