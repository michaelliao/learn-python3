import mysql.connector
import pandas as pd
import numpy as np
import re
from fractions import Fraction

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# change root password to yours:
conn = mysql.connector.connect(user='root', password='root', database='sys')

# 运行查询:
cursor = conn.cursor()
cursor.execute('SELECT * FROM `Sheet4_detail`')
values = cursor.fetchall()

# 获取查询结果的字段名
columns = [i[0] for i in cursor.description]

# 关闭 Cursor 和 Connection
cursor.close()
conn.close()

# 创建 DataFrame，并指定列名
df = pd.DataFrame(values, columns=columns)

# print(df)


# 创建中药频次字典
freq_dict = {}
for medicine in df['中药']:
    if medicine != '远志':
        if medicine in freq_dict:
            freq_dict[medicine] += 1
        else:
            freq_dict[medicine] = 1

# 对字典按频次进行排序，并取前100个
sorted_freq_dict = sorted(freq_dict.items(), key=lambda x: x[1], reverse=True)[:100]

print(sorted_freq_dict)

# 生成词云图时，指定字体
wordcloud = WordCloud(width=800, height=400, background_color='white',font_path='simhei.ttf').generate_from_frequencies(dict(sorted_freq_dict))



# 显示词云图
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()