# WEB恶意流量检测模型（第一版）
> 基于文本情感分析做的恶意http流量检测模型，属于二分类问题 
> 
> 数据集来源真实业务数据


## 模型使用
下载release中的模型，放到`model`文件夹下
针对单一流量检测，直接执行`main.py`文件即可

## 文件说明
### 训练数据文件格式
```json
{
  "feature": "package",
  "label": 0
}
```
`feature` 为数据包，分为str和package类型，str类型无换行(\n), package有换行

`label` 0为正常流量，1为恶意流量

应放在`./data/`文件夹下，该目录下应存在`train`，`test`两个目录用来存放训练集和测试集

### 语料处理
`package_sequence.py` 是语料模型

`ps_save.py` 是语料处理
> 准备好数据集之后，可以通过修改ps_save.py中的path路径，来进行语料映射模型的生成

### 数据集处理 
`dataset.py` 文件

### 流量预处理
`data_process.py` 将流量进行预处理，删除一些无意义的字段

### 流量检测
`check.py` 提供了单一流量流量检测，以及目录批量检测两种方法

### 模型训练
`model.py` 创建了模型的类，以及训练和测试方法

