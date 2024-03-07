#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, timezone

# 获取当前datetime:
now = datetime.now()
print('now =', now)
print('type(now) =', type(now))

# 用指定日期时间创建datetime:
dt = datetime(2015, 4, 19, 12, 20)
print('dt =', dt)

# 把datetime转换为timestamp:
print('datetime -> timestamp:', dt.timestamp())

# 把timestamp转换为datetime:
t = dt.timestamp()
print('timestamp -> datetime:', datetime.fromtimestamp(t))
print('timestamp -> datetime as UTC+0:', datetime.utcfromtimestamp(t))

# 从str读取datetime:
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print('strptime:', cday)

# 把datetime格式化输出:
print('strftime:', cday.strftime('%a, %b %d %H:%M'))

# 对日期进行加减:
print('current datetime =', cday)
print('current + 10 hours =', cday + timedelta(hours=10))
print('current - 1 day =', cday - timedelta(days=1))
print('current + 2.5 days =', cday + timedelta(days=2, hours=12))

# 把时间从UTC+0时区转换为UTC+8:
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
utc8_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print('UTC+0:00 now =', utc_dt)
print('UTC+8:00 now =', utc8_dt)

import datetime

target_date = datetime.datetime(2024, 2, 2, 18, 0, 0)  # 目标日期和时间
current_datetime = datetime.datetime.now()  # 当前日期和时间

time_left = target_date - current_datetime  # 计算剩余时间
time_left = max(time_left, datetime.timedelta(0))  # 确保剩余时间不为负值

# 提取剩余时间的小时、分钟和秒
hours, remainder = divmod(time_left.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)

# 输出倒计时信息
print(f"当前时间与2024-02-02 18:00:00之间相隔 {int(hours)} 小时 {int(minutes)} 分钟 {int(seconds)} 秒")
