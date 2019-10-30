#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading


# 创建全局ThreadLocal对象
local_school = threading.local()


def process_student():
    """获取当前线程关联的student"""
    student_name = local_school.student
    print(f"Hello, {student_name}(in {threading.current_thread().name})")


def process_thread(student_name):
    """绑定ThreadLocal的student"""
    local_school.student = student_name
    process_student()


t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
