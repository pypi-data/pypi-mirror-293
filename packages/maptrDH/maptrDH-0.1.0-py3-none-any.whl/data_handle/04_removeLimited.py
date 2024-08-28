import os
import numpy as np
import laspy

def extract_number(filename):
    """从文件名中提取数字部分"""
    number_str = ''
    for char in filename:
        if char.isdigit():
            number_str += char
        elif number_str:
            continue
    if number_str:
        return int(number_str)
    return None

def remove_overLimit(folder_a, folder_b, folder_c):
    for filename_a in os.listdir(folder_a):
        if filename_a.endswith(".bin"):
            filename_b = filename_a.replace("_new.bin", ".traj")
            filename_c = filename_a.replace(".bin", ".bin")
            file_path_a = os.path.join(folder_a, filename_a)
            file_path_b = os.path.join(folder_b, filename_b)
            
            if not os.path.exists(file_path_b):
                print(f"文件 {file_path_b} 不存在，跳过该文件")
                continue
            points_a = np.fromfile(file_path_a, dtype=np.float32).reshape(-1, 4) 
            # # 读取文件夹 A 中的点云数据
            # las_data = laspy.read(file_path_a)
            # # 提取点云数据
            # x = las_data.x
            # y = las_data.y
            # z = las_data.z
            # intensity = las_data.intensity  # 假设强度是第四个维度

            # # 将数据转换为numpy数组以便进一步处理
            # points_a = np.vstack((x, y, z, intensity)).transpose()       
            
            # 读取文件夹 B 中的轨迹数据
            with open(file_path_b, 'r') as file:
                lines = file.readlines()
            
            max_z = float('-inf')
            min_z = float('inf')
            
            # 解析每一行，并找到 z 坐标的最大值和最小值
            for line in lines:
                parts = line.strip().split(',')
                z_val = float(parts[2])
                if z_val > max_z:
                    max_z = z_val
                if z_val < min_z:
                    min_z = z_val

            # 筛选 points_a 中 z 值在 [min_z, max_z] 范围内的点
            filtered_points = points_a[points_a[:, 2] <= max_z + 0.01]
            # filtered_points = points_a[points_a[:, 2] >=min_z - 5.01]
            file_path_c = os.path.join(folder_c, filename_c)
            # 将筛选后的点云数据写入文件夹 C 中的文件
            filtered_points.astype(np.float32).tofile(file_path_c)

            print(f"已处理文件 {file_path_a} 并保存到 {file_path_c}")

if __name__ == "__main__":
    folder_a = '/root/autodl-fs/MapTR1/data/custom/train_0.3/bin'  # .las格式   
    folder_b = "/root/autodl-fs/MapTR1/data/custom/traj_0.3"  # 替换为文件夹 B 的路径     
    folder_c = "/root/autodl-fs/MapTR1/data/custom/train_0.3/afterRemoved"  

    # 创建输出文件夹如果不存在
    if not os.path.exists(folder_c):
        os.makedirs(folder_c)
        
    remove_overLimit(folder_a, folder_b, folder_c)
