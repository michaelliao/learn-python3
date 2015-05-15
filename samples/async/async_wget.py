#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import asyncio

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    print('current thread: %s' % threading.current_thread())
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()

loop = asyncio.get_event_loop()
tasks = [asyncio.async(wget(host)) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
for task in tasks:
    loop.run_until_complete(task)
loop.close()
print('main thread: %s' % threading.current_thread())
