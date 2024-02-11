from collections import Counter  
import pandas as pd
import re
import pymysql
import numpy as np
import jieba
from wordcloud import WordCloud
from PIL import Image
import re
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter

def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        lines = [line.rstrip("\n") for line in lines]
    return lines


def extract():
    # 读取json文件
    content_lines = read_file('D:/Documents/WeChat Files/wxid_lsootbrkhf4x22/FileStorage/File/2024-02/38988759337@chatroom_0_5539.json')

    # 将聊天记录保存到txt文件中
    with open('原始聊天记录chatroom_0_5539.txt', 'w+', encoding='utf-8') as file:
        for line in content_lines:
            file.write(line + '\n')


# 对聊天记录进行处理


def process():
    emoj_regx = re.compile(r"\[[^\]]+\]")  # 匹配表情图片
    wxid_regx = re.compile(r"wxid.*")
    english_regx = re.compile(r"[a-zA-Z]+")  # 匹配英文字符
    chinese_regx = re.compile(r"[^\u4e00-\u9fa5]+")  # 匹配非中文字符
    chinese_regx_txt = re.compile(r"表情|图片|未知|文本|时长|逼|秒|撤回|没意思|翻译结果|用户上传的GIF表情|卡片式链接|带有引用的文本消息")  # 匹配中文字符“表情”和“图片”

    space_regx = re.compile(r"\s+")  # 匹配空格
    digit_regx = re.compile(r"\d+")  # 匹配数字
    content_lines = read_file('.\原始聊天记录chatroom_0_5539.txt')
    for i in range(len(content_lines)):
        content_lines[i] = emoj_regx.sub(r"", content_lines[i])  # 去除表情图片
        content_lines[i] = wxid_regx.sub(r"", content_lines[i])
        content_lines[i] = english_regx.sub(r"", content_lines[i])  # 去除英文字符
        content_lines[i] = chinese_regx.sub(r"", content_lines[i])  # 去除非中文字符
        content_lines[i] = chinese_regx_txt.sub(r"", content_lines[i])  # 去除非中文字符
        content_lines[i] = space_regx.sub(r"", content_lines[i])  # 去除空格
        content_lines[i] = digit_regx.sub(r"", content_lines[i])  # 去除数字
    content_lines = [line for line in content_lines if line != '']

    return content_lines



def cut(content_lines):
    jieba.load_userdict('.\原始聊天记录chatroom_0_5539.txt')
    stopwords = read_file('stopwords.dat')
    all_words = []
    for line in content_lines:
        all_words += [word for word in jieba.cut(line) if word not in stopwords]
    # 使用Counter计算所有词频
    all_word_freq = Counter(all_words)
    # 过滤掉出现次数小于等于10的词
    dict_words = {word: count for word, count in all_word_freq.items() if count > 10}
    return dict_words


def get_cloud(sorted_words):
    word_counts = Counter(dict(sorted_words))
   # 保存词云图，只生成一张图，指定长宽161.8:100
    wordcloud = WordCloud(background_color='white', mask=None, font_path='simhei.ttf', stopwords=STOPWORDS, width=809, height=500)
    wordcloud.generate_from_frequencies(word_counts)
    plt.figure(figsize=(8.09, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
 


if __name__ == '__main__':
    extract()
    # 聊天记录处理
    content_lines = process()
    # 分词和停用词去除
    dict_words = cut(content_lines)
    # 降序排序，并过滤掉出现次数小于等于10的词
    sorted_words = sorted(dict_words.items(), key=lambda item: item[1], reverse=True)
    print(sorted_words)
    
    # 词云生成
    get_cloud(sorted_words)