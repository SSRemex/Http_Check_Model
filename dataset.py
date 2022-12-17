import torch
from torch.utils.data import Dataset, DataLoader
from data_process import package_format
import json
import os
import config
import numpy


class PackageDataset(Dataset):
    def __init__(self, train=True, path=None):
        if path is None:
            self.train_data_path = r"./data/train"
            self.test_data_path = r"./data/test"
            data_path = self.train_data_path if train else self.test_data_path
        else:
            data_path = path

        self.total_file_path = [os.path.join(data_path, file) for file in os.listdir(data_path)]

    def __getitem__(self, index):
        file_path: str = self.total_file_path[index]
        with open(file_path, "r", encoding="utf8") as f:
            file = f.read()
        package = json.loads(file)
        feature = package_format(package.get("feature"))
        label = package.get("label")
        return feature,  label

    def __len__(self):
        return len(self.total_file_path)


def collect_fn(batch):
    """
    :param batch:按照batch_size 传进来的 [[content, label]]
    :return:
    """
    batch_package, batch_label = list(zip(*batch))
    # 序列化
    batch_package = [config.ps.transform(package, max_len=config.MAX_LEN) for package in batch_package]
    batch_package = torch.LongTensor(batch_package)
    batch_label = torch.LongTensor(batch_label)

    return batch_package, batch_label


def get_dataloader(train=True, path=None):
    package_dataset = PackageDataset(train, path)
    dataloader = DataLoader(package_dataset, batch_size=config.BATCH_SIZE, shuffle=True, collate_fn=collect_fn)

    return dataloader


if __name__ == '__main__':
    data_loader = get_dataloader()

    # for index, (feature, label) in enumerate(data_loader):
    #     print(feature)
    #     print(label)
    #
    #     break

    print(len(data_loader))
