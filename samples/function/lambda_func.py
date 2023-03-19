#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#  Lambda functions are called anonymous functions because they don't have a name,
#  and they are not defined with the def keyword. Instead,
#  they are defined using the lambda keyword followed by a list of arguments,
#  a colon, and an expression that is evaluated and returned as the result of the function.

# Example 1
# this is a simplest example of a lambda function that inputs an integer and returns its square
unknownSquarer_func = lambda x: x*2

print(unknownSquarer_func(2))  # --> 4


# Example 2

# iterable list

numList = [1,2,3,4,5]

# this lambda function is the function that will be applied to each item in iterable using map keyword

squaredNumbers = map(lambda x:x*2,numList)

print(list(squaredNumbers))