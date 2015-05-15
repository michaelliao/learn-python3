#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server

from hello import application

httpd = make_server('', 8000, application)
print('Serving HTTP on port 8000...')

httpd.serve_forever()
