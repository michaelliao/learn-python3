
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
