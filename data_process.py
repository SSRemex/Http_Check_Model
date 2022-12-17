import os
import json
import urllib.parse
from config import SPECIAL_CHAR
from tqdm import tqdm
import re


# 流量格式化分词
def package_format(package, mode="str"):
    # url 解码
    package = urllib.parse.unquote(package)
    # 数据过滤
    # 过滤连续16位以上的字母数组-组合
    package = re.sub(r"[a-zA-z0-9\-]{16,}", " ", package, flags=re.I)
    # 过滤6位以上连续数字
    package = re.sub(r"\d{6,}", " ", package, flags=re.I)
    # 删除 cookie referer host accept xff
    if mode == "str":
        package = re.sub(r"cookie:.*?:", " ", package, flags=re.I)
        package = re.sub(r"referer:.*? ", " ", package, flags=re.I)
        package = re.sub(r"host:.*? ", " ", package, flags=re.I)
        package = re.sub(r"accept:.*? ", " ", package, flags=re.I)
        package = re.sub(r"x-forwarded-for:.*? ", " ", package, flags=re.I)

    elif mode == "package":
        package = re.sub(r"cookie:.*?\n", " ", package, flags=re.I)
        package = re.sub(r"referer:.*?\n", " ", package, flags=re.I)
        package = re.sub(r"host:.*?\n", " ", package, flags=re.I)
        package = re.sub(r"accept:.*?\n", " ", package, flags=re.I)
        package = re.sub(r"x-forwarded-for:.*?\n", " ", package, flags=re.I)
        package = package.replace("\n", " ")

    # 特殊字符处理
    for char in SPECIAL_CHAR:
        package = package.replace(char, " " + char + " ")

    tokens = [i.strip() for i in package.split() if i != ""]
    return tokens


# 训练原始宽表恶意数据处理
def malicious_data():
    with open("./data/source/宽表恶意流量.txt", encoding="utf8") as f:
        # 第一行忽略
        f.readline()
        lines = f.readlines()

        index = 0
        for line in tqdm(lines):
            content = line.split("	")
            # print(content)
            package = content[26]
            data_info = {
                "feature": package,
                "label": 1
            }
            # print(data_info)
            if index > 175000:
                with open("./data/test/1_" + str(index) + ".json", "w") as j:
                    j.write(json.dumps(data_info))
            else:
                with open("./data/train/1_" + str(index) + ".json", "w") as j:
                    j.write(json.dumps(data_info))
            index += 1


# 训练原始正常原始流量处理
def normal_data():
    with open("./data/source/正常流量.txt", encoding="utf8") as f:
        # 第一行忽略
        f.readline()
        lines = f.readlines()[200000:209000]

        index = 0
        for line in tqdm(lines):
            content = line.split("	")
            # print(content)
            package = content[7]
            data_info = {
                "feature": package,
                "label": 0
            }
            # print(data_info)
            if index > 7500:
                with open("./data/灰度check训练集/test/0_" + str(index) + ".json", "w") as j:
                    j.write(json.dumps(data_info))
            else:
                with open("./data/灰度check训练集/train/0_" + str(index) + ".json", "w") as j:
                    j.write(json.dumps(data_info))
            index += 1


# 检测流量处理
def check_data(path, label):
    with open(path, encoding="utf8") as f:
        f.readline()
        lines = f.readlines()
        index = 0
        for line in tqdm(lines):
            content = line.split("	")
            # print(content)
            package = content[7]
            data_info = {
                "feature": package,
                "label": label
            }
            # print(data_info)
            if index > 7500:
                with open("./data/灰度check训练集/test/1_" + str(index) + ".json", "w") as j:
                    j.write(json.dumps(data_info))
            else:
                with open("./data/灰度check训练集/train/1_" + str(index) + ".json", "w") as j:
                    j.write(json.dumps(data_info))

            index += 1


if __name__ == '__main__':

    # malicious_data()
    normal_data()
    check_data("./data/source/灰度恶意流量.txt", label=1)




