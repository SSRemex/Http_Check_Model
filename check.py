import config
from data_process import package_format
import torch
from model import WafCheckModel
from dataset import get_dataloader
import numpy
import time


# 传入模型
model = WafCheckModel()
model.load_state_dict(torch.load("waf_model.pkl"))


def one_package_check(package, mode="package"):
    # 分词处理
    package_tokenize = package_format(package, mode="package")
    # print(package_tokenize)
    # 序列化
    package_transform = config.ps.transform(package_tokenize, max_len=config.MAX_LEN)

    package_transform = torch.tensor(package_transform).reshape(1, -1)

    # 查看结果
    label = model(package_transform)
    label = label.max(dim=-1)[-1]
    print(label)
    if label.item() == 0:
        print("正常流量")
    else:
        print("恶意流量")


def all_package_check(path):
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


if __name__ == '__main__':
    all_package_check(path="./data/灰度check训练集/train")
    # package = "GET /?bid=ca5990264a164e1f9b3ea391deedac95&id=1+union+select+current+schema+from+sysibm.sysdummy1 HTTP/1.1             rm-pro-time:1670575793282             x-forwarded-for:42.187.174.228             x-scheme:https             x-real-ip:42.187.174.228             accept-encoding:gzip,deflate             host:appseccheck.58.com             x-forwarded-proto:https             https-tag:HTTPS             rm-pro-token:             rm-pro-businessid:ca5990264a164e1f9b3ea391deedac95             x-remote-port:54067             user-agent:curl/7.83.1"
    # one_package_check(package=package, mode="str")

