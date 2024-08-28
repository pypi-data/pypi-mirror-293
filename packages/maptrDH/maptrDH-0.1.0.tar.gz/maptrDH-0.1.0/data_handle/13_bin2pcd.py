import os
import numpy as np
import struct
import open3d as o3d

def read_bin_file(file_path):
    """读取二进制点云文件"""
    with open(file_path, 'rb') as f:
        data = f.read()
    # 解析二进制数据
    num_points = len(data) // 16  # 每个点由4个float32组成，每个float32占4个字节
    points = np.array(struct.unpack('f' * num_points * 4, data)).reshape(-1, 4)  # 解析成点的形式
    return points

def batch_convert_bin_to_pcd(input_folder, output_folder):
    """批量转换二进制点云文件到PCD文件"""
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.bin'):
            # 构建输入和输出文件的完整路径
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace('.bin', '.pcd'))

            # 读取二进制点云文件
            points = read_bin_file(input_file_path)
            points_pcd = points[:, 0:3]
            # 构建点云对象
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points_pcd)  # 无需切片，直接赋值点云数据
            intensity = points[:,3].astype(np.float64)  # 将强度信息转换为浮点数类型
            if np.max(intensity) != 0:
                intensity /= np.max(intensity)
                pcd.colors = o3d.utility.Vector3dVector(np.vstack((intensity, intensity, intensity)).T)
            # Save to whatever format you like
            o3d.io.write_point_cloud(output_file_path, pcd)
            print("转换完成：", filename)

# 调用批量转换函数
# input_folder_a = '/root/autodl-fs/MapTR1/data/custom/try_RL/CHECK2'  # 文件夹A中的二进制点云文件
# output_folder_a = '/root/autodl-fs/MapTR1/data/custom/try_RL/CHECK2'  # 保存转换后的PCD文件的文件夹A
input_folder_a = r'/autodl-fs/data/MapTR1/data/custom/test_of_test/after_translated'
output_folder_a = r'/autodl-fs/data/MapTR1/data/custom/test_of_test/pcd'                                    
batch_convert_bin_to_pcd(input_folder_a, output_folder_a)

print("全部转换完成！")
