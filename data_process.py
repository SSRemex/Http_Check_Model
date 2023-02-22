import urllib.parse
from config import SPECIAL_CHAR
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





