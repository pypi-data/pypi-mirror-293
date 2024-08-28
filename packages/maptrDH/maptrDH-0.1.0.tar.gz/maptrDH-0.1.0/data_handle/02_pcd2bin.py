import numpy as np
from pypcd import pypcd
import os

input_folder = '/root/autodl-fs/MapTR1/data/custom/train_0.3/pcd'  # 输入文件夹，包含PCD文件                
output_folder = '/root/autodl-fs/MapTR1/data/custom/train_0.3/bin'  # 输出文件夹，保存转换后的LAS文件              
i=1
# Iterate over each .pcd file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.pcd'):
        if "_new" not in filename:
            print(i)
            i=i+1
            pcd_path = os.path.join(input_folder, filename)
            pcd_data = pypcd.PointCloud.from_path( pcd_path)
            points = np.zeros([pcd_data.width, 4], dtype=np.float32)
            points[:, 0] = pcd_data.pc_data['x'].copy()
            points[:, 1] = pcd_data.pc_data['y'].copy()
            points[:, 2] = pcd_data.pc_data['z'].copy()
            points[:, 3] = pcd_data.pc_data['rgb'].copy().astype(np.float32)
            bin_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '_new.bin')
            with open(bin_file, 'wb') as f:
                f.write(points.tobytes())
print("end")
