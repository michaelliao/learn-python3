import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件数据
df = pd.read_csv(r'D:\pyspace\learn-python3\samples\matplotlib\中医症候.csv')

# 设置中文显示的字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 若百分比数据为字符串形式，需要将其转换为数值形式
# 此行代码假设百分比列的值包含%符号，如'22.42%'
df['百分比'] = df['百分比'].str.rstrip('%').astype('float')

# 绘制图表
fig, ax = plt.subplots(figsize=(12, 6))

# 以天蓝色作为颜色绘制频次柱状图
ax.bar(df['中医证候'], df['频次'], color='skyblue')

# 设置坐标轴标签
# ax.set_xlabel('中医证候')
ax.set_ylabel('频次')

# 以红色圆圈绘制百分比折线图
ax2 = ax.twinx()
ax2.plot(df['中医证候'], df['百分比'], 'ro-')
ax2.set_ylabel('百分比 (%)')

# 去掉网格线
ax.grid(False)

# 在每个柱子上方标识频次数量值
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, 
            bar.get_height(), 
            '{:.0f}'.format(bar.get_height()), 
            ha='center', 
            va='bottom')

# 调整整体空白，防止标签重叠
fig.tight_layout()

# 显示图表
plt.show()
