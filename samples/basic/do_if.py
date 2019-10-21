#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# bada:
# input() Restituisce una stringa
# Deve passare int() Converte una stringa in un numero intero
# Può essere utilizzato per il confronto numerico:
age = int(input('Input your age: '))

if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')
