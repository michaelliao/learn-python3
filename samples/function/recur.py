#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 利用递归函数计算阶乘
# N! = 1 * 2 * 3 * ... * N
def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)

print('fact(1) =', fact(1))
print('fact(5) =', fact(5))
print('fact(10) =', fact(10))

# 利用递归函数移动汉诺塔:
def move(n, a, b, c):
    if n == 1:
        print('move', a, '-->', c)
    else:
        move(n-1, a, c, b)
        move(1, a, b, c)
        move(n-1, b, a, c)

move(4, 'A', 'B', 'C')



global index
index = 0
def __move(mark, from_,to):
    global index
    index =index + 1
    print('步骤：',index,'盘子编号：',mark,from_,'->',to )

def hannoi(n,start,end,middle):
    if n==1 :
        __move(n,start ,end )
    else:
        hannoi(n-1,start,middle,end )
        __move(n,start,end )
        hannoi(n-1,middle,end,start)


hannoi(4,'start','end','middle')
