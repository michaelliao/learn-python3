from collections import Counter  
import pandas as pd
import re
import pymysql
import numpy as np
import jieba
from wordcloud import WordCloud
from PIL import Image


def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        lines = [line.rstrip("\n") for line in lines]
    return lines


# 从message表提取原始聊天记录并保存
def extract():
    # 连接到MySQL数据库
    conn = pymysql.connect(host='localhost', port=3308, user='root', password='root', database='demo')
 
    cursor = conn.cursor()
    cursor.execute('SELECT JSON_EXTRACT(content, "$.msg") AS msg_value  FROM wxid_p34mlvra9brc22_0_20230207_20240201 WHERE talker = "我";')
    contents = cursor.fetchall()

    with open('原始聊天记录me.txt', 'w+', encoding='utf-8') as file:
        for content in contents:
            file.write(content[0] + '\n')

    cursor.close()
    conn.close()


# 对聊天记录进行处理
def process():
    emoj_regx = re.compile(r"\[[^\]]+\]")  # 匹配表情图片
    wxid_regx = re.compile(r"wxid.*")
    english_regx = re.compile(r"[a-zA-Z]+")  # 匹配英文字符
    chinese_regx = re.compile(r"表情|图片|未知|时长|逼|秒|撤回|没意思|翻译结果|用户上传的GIF表情|卡片式链接|带有引用的文本消息")  # 匹配中文字符“表情”和“图片”
    space_regx = re.compile(r"\s+")  # 匹配空格
    digit_regx = re.compile(r"\d+")  # 匹配数字
    content_lines = read_file('原始聊天记录me.txt')
    for i in range(len(content_lines)):
        content_lines[i] = emoj_regx.sub(r"", content_lines[i])  # 去除表情图片
        content_lines[i] = wxid_regx.sub(r"", content_lines[i])
        content_lines[i] = english_regx.sub(r"", content_lines[i])  # 去除英文字符
        content_lines[i] = chinese_regx.sub(r"", content_lines[i])  # 去除中文字符“表情”和“图片”
        content_lines[i] = space_regx.sub(r"", content_lines[i])  # 去除空格
        content_lines[i] = digit_regx.sub(r"", content_lines[i])  # 去除数字
    content_lines = [line for line in content_lines if line != '']

    return content_lines


def cut(content_lines):
    jieba.load_userdict('./原始聊天记录me.txt')
    stopwords = read_file('./stopwords.dat')
    all_words = []
    for line in content_lines:
        all_words += [word for word in jieba.cut(line) if word not in stopwords]
    # 使用Counter计算所有词频
    all_word_freq = Counter(all_words)
    # 过滤掉出现次数小于等于10的词
    dict_words = {word: count for word, count in all_word_freq.items() if count > 10}
    return dict_words

def get_cloud(sorted_words, num):
    mask_image = np.array(Image.open('muban3.png'))
    word_counts = Counter(dict(sorted_words))
    chunk_size = len(sorted_words) // num  # 总词数除以词云图数量
    
    for i in range(num):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num - 1 else len(sorted_words)  # 确保最后一个chunk包含所有剩余的词
        chunk = {word: count for word, count in sorted_words[start:end]}
        
        wordcloud = WordCloud(background_color='white', mask=mask_image, font_path='simhei.ttf')
        wordcloud.generate_from_frequencies(chunk)
        wordcloud.to_file('./me/cloud0{}.png'.format(i + 1))  # 保存词云图，文件名按1开始编号

if __name__ == '__main__':
    # 提取聊天记录
    extract()
    # 聊天记录处理
    content_lines = process()
    # 分词和停用词去除
    dict_words = cut(content_lines)
    # 降序排序，并过滤掉出现次数小于等于10的词
    sorted_words = sorted(dict_words.items(), key=lambda item: item[1], reverse=True)
    print(sorted_words)
    
    # 词云生成
    # 确保按照词频超过十次的词来构成五张词云图
    get_cloud(sorted_words, 5)