import config
from data_process import package_format
import torch
from model import WafCheckModel
from dataset import get_dataloader
import numpy
import time


# 传入模型
start = time.time()
model = WafCheckModel()
model.load_state_dict(torch.load("model/waf_model.pkl"))
end = time.time()
print(f"模型加载时间：{end-start}")


def one_package_check(package, mode="package"):
    """
    :param package: 待检测流量字段
    :param mode: 数据包格式（换行） 字符串格式（无换行）
    :return:
    """
    # 分词处理
    package_tokenize = package_format(package, mode=mode)
    # print(package_tokenize)
    # 序列化
    package_transform = config.ps.transform(package_tokenize, max_len=config.MAX_LEN)

    package_transform = torch.tensor(package_transform).reshape(1, -1)

    # 查看结果
    label = model(package_transform)
    label = label.max(dim=-1)[-1]
    if label.item() == 0:
        print("正常流量")
    else:
        print("恶意流量")


def all_package_check(path):
    """
    对一个路径下的所有数据文件进行批量检测
    :param path: 待检测文件路径
    :return:
    """
    print("开始检测")
    start = time.time()
    loss_list = []
    acc_list = []
    data_loader = get_dataloader(train=False, path=path)
    for index, (feature, label) in enumerate(data_loader):
        feature = feature
        label = label
        with torch.no_grad():
            pre_label = model(feature)
            cur_loss = torch.nn.functional.nll_loss(pre_label, label)
            # 转为CPU
            loss_list.append(cur_loss.cpu().item())
            # 计算准确率
            pred = pre_label.max(dim=-1)[-1]
            cur_acc = pred.eq(label).float().mean()
            acc_list.append(cur_acc.cpu().item())
            print(f"index: {index} loss: {cur_loss.item()} acc: {cur_acc.item()}")
    end = time.time()

    print(f"total loss: {numpy.mean(loss_list)}, accuracy: {numpy.mean(acc_list)}")
    print(f"cost: {int(end - start)}")



