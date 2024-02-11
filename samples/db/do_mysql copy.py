#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########## prepare ##########

# install mysql-connector-python:
# pip3 install mysql-connector-python --allow-external mysql-connector-python

import mysql.connector
import pandas as pd
import numpy as np
import re
from fractions import Fraction

# change root password to yours:
conn = mysql.connector.connect(user='root', password='root', database='sys')

# 运行查询:
cursor = conn.cursor()
cursor.execute('SELECT a.患者编号,姓名,性别,年龄,就诊日期,既往史,并发症,临床表现,舌质,中药组成,中药,克数 FROM Sheet4 a LEFT JOIN Sheet4_detail b ON a.`患者编号`=b.`患者编号`')
values = cursor.fetchall()

# 获取查询结果的字段名
columns = [i[0] for i in cursor.description]

# 关闭 Cursor 和 Connection
cursor.close()
conn.close()

# 创建 DataFrame，并指定列名
df = pd.DataFrame(values, columns=columns)
# print(df)



## 1.	远志、石菖蒲、川芎的用量及用量的频次、频率，平均用量
print("1.	远志、石菖蒲、川芎的用量及用量的频次、频率，平均用量")
# 将克数转换为数字
df['克数'] = df['克数'].str.extract('(\d+)').astype(float)

# 筛选出远志、石菖蒲、川芎的数据
selected_herbs = ['远志', '石菖蒲', '川芎']
selected_df = df[df['中药'].isin(selected_herbs)]

# 获取用量及用量的频次
usage_info = selected_df.groupby('中药')['克数'].agg(['sum', 'count'])

# 计算平均用量
usage_info['平均用量'] = usage_info['sum'] / usage_info['count']

# 重命名列名
usage_info = usage_info.rename(columns={'sum': '用量总和', 'count': '用量频次'})

# print(usage_info)

# 验证 1 MySQL，验证通过
# SELECT
#     COUNT(1) AS total_count,
#     SUM(CAST(REPLACE(c.克数, 'g', '') AS SIGNED)) AS sum_of_numbers
# FROM
#     (
#         SELECT a.患者编号,姓名,性别,年龄,就诊日期,既往史,并发症,临床表现,舌质,中药组成,中药,克数
#         FROM Sheet4 a
#         LEFT JOIN Sheet4_detail b ON a.`患者编号` = b.`患者编号`
#     ) AS c 
# WHERE
#     c.`中药` = '石菖蒲';


#

## 2.	远志与石菖蒲、远志与川芎用量比例及比例的频次、频率
print(" 2.	远志与石菖蒲、远志与川芎用量比例及比例的频次、频率 ") 


# 为远志与石菖蒲、远志与川芎创建透视表
# pivot_table = df.pivot_table(index='患者编号', columns='中药', values='克数', aggfunc='sum', fill_value=0)
# 是用来指定在执行 unstack 操作时，对于缺失值（NaN）的填充值
pivot_table = df.groupby(['患者编号', '中药'])['克数'].sum().unstack(fill_value=0)

# 计算远志与石菖蒲的用量比例
pivot_table['远志:石菖蒲比例'] = pivot_table['远志'] / pivot_table['石菖蒲']
pivot_table['远志:石菖蒲比例'] = pivot_table['远志:石菖蒲比例'].replace([np.inf, -np.inf, np.nan], 0).round(2)


# 获取远志与石菖蒲比例的频次和频率
pivot_table_prop1 = pivot_table['远志:石菖蒲比例']
count_vc1 = pivot_table['远志:石菖蒲比例'].value_counts().sort_index()
freq_vc1 = count_vc1 / count_vc1.sum() * 100

# 将 pivot_table_prop1 转换为 DataFrame
df_prop1 = pivot_table_prop1.reset_index()
df_prop1.columns = ['患者编号', '远志:石菖蒲比例']

# 合并 df_prop1、count_vc1 和 freq_vc1
result_df = pd.merge(df_prop1.drop(columns='患者编号'), pd.DataFrame({'远志:石菖蒲比例频次': count_vc1}),
                     left_on='远志:石菖蒲比例', right_index=True, how='left')

result_df = pd.merge(result_df, pd.DataFrame({'远志:石菖蒲比例频率(%)': freq_vc1}),
                     left_on='远志:石菖蒲比例', right_index=True, how='left')

# 去除患者编号这一列
result_df = result_df[['远志:石菖蒲比例', '远志:石菖蒲比例频次', '远志:石菖蒲比例频率(%)']]

# 格式化 '远志:石菖蒲比例' 列
result_df['远志:石菖蒲比例'] = result_df['远志:石菖蒲比例'].apply(
    lambda x: f"{Fraction(x).limit_denominator()}" if not pd.isna(x) and x != float('inf') else 'Infinity')


# 基于 '远志:石菖蒲比例' 列分组，取每组的第一个值
grouped_result_df = result_df.groupby('远志:石菖蒲比例').first()

# 输出结果
print(grouped_result_df)

# 计算远志与川芎的用量比例
pivot_table['远志:川芎比例'] = pivot_table['远志'] / pivot_table['川芎']
pivot_table['远志:川芎比例'] = pivot_table['远志:川芎比例'].replace([np.inf, -np.inf, np.nan], 0).round(2)
# 获取远志与石菖蒲比例的频次和频率
pivot_table_prop2 = pivot_table['远志:川芎比例']
# 获取远志与川芎比例的频次和频率
count_vc2 = pivot_table['远志:川芎比例'].value_counts().sort_index()
freq_vc2 = count_vc2 / count_vc2.sum() * 100

# 将 pivot_table_prop2 转换为 DataFrame
df_prop2 = pivot_table_prop2.reset_index()
df_prop2.columns = ['患者编号', '远志:川芎比例']

# 合并 df_prop2、count_vc2 和 freq_vc1
result_df2 = pd.merge(df_prop2.drop(columns='患者编号'), pd.DataFrame({'远志:川芎比例频次': count_vc2}),
                     left_on='远志:川芎比例', right_index=True, how='left')

result_df2 = pd.merge(result_df2, pd.DataFrame({'远志:川芎比例频率(%)': freq_vc2}),
                     left_on='远志:川芎比例', right_index=True, how='left')


result_df2['远志:川芎比例'] = result_df2['远志:川芎比例'].apply(lambda x: f"{Fraction(x).limit_denominator()}" if not pd.isna(x) and x != float('inf') else 'Infinity')

# 基于 '远志:石菖蒲比例' 列分组，取每组的第一个值
grouped_result_df2 = result_df2.groupby('远志:川芎比例').first()
# 输出结果
print(grouped_result_df2)


## 3.	远志与石菖蒲、远志与川芎用量比例归纳表 
print(" 3.	远志与石菖蒲、远志与川芎用量比例归纳表 ")

# 选取远志、石菖蒲和川芎的数据
selected_herbs = ['远志', '石菖蒲', '川芎']
selected_df = df[df['中药'].isin(selected_herbs)]

# 计算远志与石菖蒲的用量比例
yunzhi_shichangpu = selected_df[selected_df['中药'].isin(['远志', '石菖蒲'])].groupby('患者编号')['克数'].agg('sum')
yunzhi_shichangpu_ratio = yunzhi_shichangpu.div(yunzhi_shichangpu.sum())

# 计算远志与川芎的用量比例
yunzhi_chuanxiong = selected_df[selected_df['中药'].isin(['远志', '川芎'])].groupby('患者编号')['克数'].agg('sum')
yunzhi_chuanxiong_ratio = yunzhi_chuanxiong.div(yunzhi_chuanxiong.sum())

# 创建归纳表
summary_table = pd.DataFrame(index=['<1', '=1', '>1'])

# 添加远志与石菖蒲的用量比例信息
summary_table['远志:石菖蒲 频次'] = pd.cut(yunzhi_shichangpu_ratio, bins=[0, 0.1, 0.2, 1], labels=['<1', '=1', '>1']).value_counts().sort_index()
summary_table['远志:石菖蒲 频率(%)'] = (summary_table['远志:石菖蒲 频次'] / summary_table['远志:石菖蒲 频次'].sum() * 100).round(2)

# # 添加远志与川芎的用量比例信息
# summary_table['远志:川芎 频次'] = pd.cut(yunzhi_chuanxiong_ratio, bins=[0, 0.1, 0.2, 1], labels=['<1', '=1', '>1']).value_counts().sort_index()
# summary_table['远志:川芎 频率(%)'] = (summary_table['远志:川芎 频次'] / summary_table['远志:川芎 频次'].sum() * 100).round(2)

# print(summary_table)
