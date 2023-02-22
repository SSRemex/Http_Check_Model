import time

import torch
import config
import os
from dataset import get_dataloader
import numpy

from tqdm import tqdm


class WafCheckModel(torch.nn.Module):
    def __init__(self):
        super(WafCheckModel, self).__init__()
        self.embedding = torch.nn.Embedding(len(config.ps), 100)
        self.lstm = torch.nn.LSTM(input_size=100, hidden_size=config.HIDDEN_SIZE, num_layers=config.NUM_LAYERS,
                                  batch_first=True, bidirectional=True, dropout=0.5)

        self.lstm_2 = torch.nn.LSTM(input_size=config.HIDDEN_SIZE * 2, hidden_size=config.HIDDEN_SIZE,
                                    num_layers=config.NUM_LAYERS, batch_first=True, bidirectional=False, dropout=0.5)

        self.fc = torch.nn.Linear(config.HIDDEN_SIZE, 2)

    def forward(self, feature):

        # feature: [batch_size, max_len]
        x = self.embedding(feature)
        # x: [batch_size, max_len, 200]
        x, (h_n, c_n) = self.lstm(x)
        # x: [batch_size, max_len, 2 * hidden_size] h_n: [2 *num_layer, batch_size, hidden_size]
        # 获取两个方向最后一次的output
        output_forward = h_n[-2, :, :]
        output_backward = h_n[-1, :, :]
        output = torch.cat([output_forward, output_backward], dim=-1)
        output2, (h_n2, c_n2) = self.lstm_2(output)

        out = self.fc(output2)

        return torch.nn.functional.log_softmax(out, dim=-1)


model = WafCheckModel().to(config.device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

if os.path.exists("model/waf_model.pkl"):
    model.load_state_dict(torch.load("model/waf_model.pkl"))
    optimizer.load_state_dict(torch.load("model/optimizer.pkl"))


def train(epoch):
    data_loader = get_dataloader(train=True, path="./data/灰度check训练集/train")
    for index, (feature, label) in enumerate(data_loader):
        feature = feature.to(config.device)
        label = label.to(config.device)

        optimizer.zero_grad()
        pre_label = model(feature)
        loss = torch.nn.functional.nll_loss(pre_label, label)

        loss.backward()
        optimizer.step()
        print(epoch, index, loss.item())
        if index % 100 == 1:
            torch.save(model.state_dict(), "model/waf_model.pkl")
            torch.save(optimizer.state_dict(), "model/optimizer.pkl")


def test():
    loss_list = []
    acc_list = []
    data_loader = get_dataloader(train=False)
    for index, (feature, label) in enumerate(data_loader):
        feature = feature.to(config.device)
        label = label.to(config.device)
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

    print(f"total loss: {numpy.mean(loss_list)}, accuracy: {numpy.mean(acc_list)}")


if __name__ == '__main__':
    start = time.time()
    for i in tqdm(range(100)):
         train(i)

    # test()
    end = time.time()
    print(f"cost {end - start}")












