#! /usr/bin/env python3.6

'''
Example for different types of string formatting available in Python >= 3.6

'''

example1 = "F String Formatting example."

example2 = ".format style formatting(available in python <3.6 as well)."

example3 = "Old style formatting from python 2.x"


print(f'{example1}')

print("{}".format(example2))

print("%s"% example3)
