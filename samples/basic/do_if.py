#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 注意:
# input()返回的是字符串
# 必须通过int()将字符串转换为整数
# 才能用于数值比较:
age = int(input('Input your age: '))

if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')

    
#practice code of this lesson
bmi = weight/(height*height)
print(bmi)

if bmi <= 18.5:
    print('too light')
elif (bmi > 18.5) & (bmi <= 25):
    print('normal')
elif (bmi > 25) & (bmi <= 28):
    print('too heavy')
elif (bmi > 28) & (bmi <= 32):
    print('fat')
else :
    print('too fat')
