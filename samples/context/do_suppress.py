#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove('tempfile.1')
    os.remove('tempfile.2')
    os.remove('tempfile.3')
