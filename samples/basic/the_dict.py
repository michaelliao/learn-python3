#!/usr/bin/env python3
# -*- coding: utf-8 -*-

d = {
    'Michael': 95,
    'Bob': 75,
    'Tracy': 85
}
print('d[\'Michael\'] =', d['Michael'])
print('d[\'Bob\'] =', d['Bob'])
print('d[\'Tracy\'] =', d['Tracy'])
print('d.get(\'Thomas\', -1) =', d.get('Thomas', -1))

# To add another name in d, example adding 'Gautam':25 to d

d.update({'Gautam':25})


print('d[\'Gautam\'] =', d['Gautam'])

