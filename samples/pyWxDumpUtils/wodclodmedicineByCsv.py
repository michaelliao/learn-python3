import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df = pd.read_csv(r'D:\pyspace\learn-python3\samples\pyWxDumpUtils\中药频次.csv')

# 去除远志
df = df[df['中药统计分析'] != '远志']

# 生成词云
wordcloud = WordCloud(
    background_color='white',
    width=1000,
    height=700,
    font_path='simhei.ttf',  # 使用中文字体
    colormap='YlGnBu'  # 设置颜色方案
).generate(df['中药统计分析'].to_string(index=False))

# 显示词云
plt.figure(figsize=(16, 9))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
