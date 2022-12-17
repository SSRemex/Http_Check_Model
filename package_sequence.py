"""
    实现构建词典，将流量转为数字序列和其反序列
"""


class Package2Sequence:

    # 未知标签
    UNK_TAG = "UNKNOWN"
    # 填充标签
    PAD_TAG = "PADDING"

    UNK = 0
    PAD = 1

    def __init__(self):
        self.dict = {
            self.UNK_TAG: self.UNK,
            self.PAD_TAG: self.PAD
        }

        self.inverse_dict = {

        }

        self.count = {}

    def fit(self, content):
        """
        统计词频
        :param content:
        :return:
        """
        for char in content:
            self.count[char] = self.count.get(char, 0) + 1

    def build_vocab(self):
        """
        生成全字符词典
        :return:
        """
        for word in self.count:
            # 给每一个word一个唯一的值
            self.dict[word] = len(self.dict)

        # 生成反转词典
        self.inverse_dict = dict(zip(self.dict.values(), self.dict.keys()))

    def transform(self, content, max_len=None):
        """
        将content数字序列化
        :param content:
        :param max_len:
        :return:
        """
        if max_len is not None:
            if max_len > len(content):
                content = content + [self.PAD_TAG] * (max_len - len(content))
            if max_len < len(content):
                content = content[:max_len]

        content = [self.dict.get(char, self.UNK) for char in content]

        return content

    def inverse_transform(self, indices):
        return [self.inverse_dict.get(idx) for idx in indices]

    def __len__(self):
        return len(self.dict)







