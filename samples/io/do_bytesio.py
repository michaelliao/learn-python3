#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import BytesIO

# write to BytesIO:
f = BytesIO()
f.write(b'hello')
f.write(b' ')
f.write(b'world!')
print(f.getvalue())

# read from BytesIO:
data = ' peopleSpendTheirSweet-ScentedOsmanthusFlowersAndTheNightIsQuietTheMoonIsAStunnedMountainBird '.encode('utf-8')
f = BytesIO(data)
print(f.read())
