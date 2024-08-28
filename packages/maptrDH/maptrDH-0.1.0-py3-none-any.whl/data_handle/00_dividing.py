import os
import random
import shutil

# 设置随机种子以复现结果
random.seed(42)

# 指定原始数据文件夹路径
source_folder = '/root/autodl-fs/MapTR1/data/custom/block_las_new'

# 指定测试集和训练集的文件夹路径
test_folder = '/root/autodl-fs/MapTR1/data/custom/test/las'
train_folder = '/root/autodl-fs/MapTR1/data/custom/train/las'

# 获取所有.bin文件
files = [file for file in os.listdir(source_folder) if file.endswith('.las')]
random.shuffle(files)  # 打乱文件列表

# 计算测试集的数量
num_test = int(0.2 * len(files))  # 20% 为测试集

# 分割文件列表
test_files = files[:num_test]
train_files = files[num_test:]

# 移动文件到相应的测试集和训练集文件夹
for file in test_files:
    shutil.move(os.path.join(source_folder, file), os.path.join(test_folder, file))

for file in train_files:
    shutil.move(os.path.join(source_folder, file), os.path.join(train_folder, file))

print(f"Moved {len(test_files)} files to {test_folder}")
print(f"Moved {len(train_files)} files to {train_folder}")
