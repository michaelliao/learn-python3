import re

# 打开文件
# with open(r"D:\Documents\WeChat Files\wxid_lsootbrkhf4x22\FileStorage\File\2024-02\报错-药店-2.txt", "r", encoding="gbk") as f:
#     data = f.read()
with open(r"D:\NeuSoftResources\海南\l_hosp_appr_info_d_药店.sql", "r", encoding="utf") as f:
    data = f.read()

# 提取数据中的 P 开头后 11 位的字符串
pattern = r"('P[0-9]{11}')"
matches = re.findall(pattern, data)

# 打印提取到的字符串
for match in matches:
    print(match)
