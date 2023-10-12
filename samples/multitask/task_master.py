#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random, time, queue, os
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
def lambda_task_queue(): return  task_queue
def lambda_result_queue(): return  result_queue


def main():
    QueueManager.register('get_task_queue', callable=lambda_task_queue)
    QueueManager.register('get_result_queue', callable=lambda_result_queue)
    # 绑定端口5000, 设置验证码'abc':
    manager = QueueManager(address=('127.0.0.1' if os.name == 'nt' else '', 5000), authkey=b'abc') # win*下host不能为''
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)
    # 关闭:
    manager.shutdown()
    print('master exit.')


if __name__ == '__main__':
    main()
