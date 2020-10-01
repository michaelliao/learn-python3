#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = input()
print('Hello,', name)

#another version of using imput fuction, where it can print a message, as well as take input from the user
name = input("Enter your name: ")
print("Hello,", name)

#When we take imput, it will be in string. So to convert into integer we can use int() 
#This code will take two numbers as imput and computes the sum and prints the result
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
sum = num1+num2
print(sum)
           
