import os
import numpy as np
import laspy

def replace_intensity(folder_a, folder_b):
    for filename_a in os.listdir(folder_a):
        if filename_a.endswith("_new.bin"):
            filename_b = filename_a.replace("_new.bin", ".las")  # 假设文件夹 B 中的文件名为文件夹 A 中文件名后加上 "_new"
            file_path_a = os.path.join(folder_a, filename_a)
            file_path_b = os.path.join(folder_b, filename_b)
            
            # 读取文件夹 A 中的点云数据
            points_a = np.fromfile(file_path_a, dtype=np.float32).reshape(-1, 4)  # 假设点云数据是以 float32 格式存储的
            
            # 读取文件夹 B 中的点云数据                     
            # 读取las文件
            inFile = laspy.read(file_path_b)
            
            # 获取点云数据
            points_b = np.vstack((inFile.x, inFile.y, inFile.z, inFile.intensity)).T  # 将x、y、z坐标堆叠成矩阵
            points_b = points_b.reshape(-1, 4)  # 假设点云数据是以 float32 格式存储的
            
            # 将文件夹 A 中的点云数据的强度信息替换为文件夹 B 中对应点云的强度信息
            points_a[:, 3] = points_b[:, 3]
            
            # 将替换后的点云数据写入文件夹 A 中的文件
            points_a.tofile(file_path_a)

            print(f"已替换文件 {file_path_a} 中的强度信息")

if __name__ == "__main__":
    folder_a = "/root/autodl-fs/MapTR1/data/custom/train_0.3/bin"  # 替换为文件夹 A 的路径                 
    folder_b = "/root/autodl-fs/MapTR1/data/custom/train_0.3/las"  # 替换为文件夹 B 的路径              

    replace_intensity(folder_a, folder_b)
