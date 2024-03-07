#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########## prepare ##########

# install mysql-connector-python:
# pip3 install mysql-connector-python --allow-external mysql-connector-python

import mysql.connector
import pandas as pd
import numpy as np
import re

# change root password to yours:
conn = mysql.connector.connect(user='root', password='root', database='sys')

# 运行查询:
cursor = conn.cursor()
cursor.execute('select 患者编号,中药组成 from Sheet4 ')
values = cursor.fetchall()

# 获取查询结果的字段名
columns = [i[0] for i in cursor.description]

# 关闭 Cursor 和 Connection
cursor.close()
conn.close()

# 创建 DataFrame，并指定列名
df = pd.DataFrame(values, columns=columns)

# 提取中文和数字字母的正则表达式
pattern = re.compile(r'([\u4e00-\u9fa5]+)(\d+\w+)')
result = df['中药组成'].str.extractall(pattern)


# 保存原始的患者编号列
patient_ids = df['患者编号'].iloc[result.index.get_level_values(0)].reset_index(drop=True)

# 重置索引
result.reset_index(drop=True, inplace=True)


# 将患者编号加回结果中
result['患者编号'] = patient_ids

# 重新排列列的顺序
result = result[['患者编号', 0, 1]]
# 重命名列名
result.columns = ['患者编号', '草药', '克数']
# 打印 result 的所有内容
print(result)

# 将数据插入新表
connInsert = mysql.connector.connect(user='root', password='root', database='sys')
cursorInsert = connInsert.cursor()

# 使用 iterrows() 迭代 DataFrame 中的行
for _, row in result.iterrows():
    cursorInsert.execute('INSERT INTO Sheet4_detail (患者编号, 中药, 克数) VALUES (%s, %s, %s)', (row['患者编号'], row['草药'], row['克数']))

# 提交更改并关闭连接
connInsert.commit()
cursorInsert.close()
connInsert.close()
