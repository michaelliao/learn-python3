#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

#create socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# establish connection:
s.connect(('www.sina.com.cn', 80))

# send data:
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# recive data:
buffer = []
while True:
    # Receive up to 1k bytes at a time:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break

data = b''.join(buffer)

# close the connection:
s.close()

header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))

# Write received data to file:
with open('sina.html', 'wb') as f:
    f.write(html)
