#!/usr/bin/env python3
# -*- coding: utf-8 -*-

age = 10

# simple one line if else expression
message = "you are too old" if age > 15 else "you are too young"

# advanced oneline if else expression
message2 = "you are too old" if age > 15 else "you are too young" if age < 4 else "you are a bit older" if age == 14 else "You are good to go" if age == 10 else "You are disqualified"

print(message2)
