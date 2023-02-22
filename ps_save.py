import json
import os
from package_sequence import Package2Sequence
from data_process import package_format
import pickle
from tqdm import tqdm


# 保存ps
ps = Package2Sequence()
# 待处理的语料数据路径
path = r"./data/train"
file_path = [os.path.join(path, file_name) for file_name in os.listdir(path)]

fail_file = []

for file in tqdm(file_path):
    try:
        with open(file, "r") as f:
            data = f.read()
            package = json.loads(data)["feature"]
            content = package_format(package)
            ps.fit(content)
    except:
        fail_file.append(file)


print(f"fail {len(fail_file)}")
for file in tqdm(fail_file):
    try:
        with open(file, "r") as f:
            data = f.read()
            package = json.loads(data)["feature"]
            content = package_format(package)
            ps.fit(content)
    except Exception as e:
        print(e)


ps.build_vocab()
pickle.dump(ps, open("model/ps.pkl", "wb"))
print(len(ps))
