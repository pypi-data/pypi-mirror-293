import os
import numpy as np
import laspy
import matplotlib.pyplot as plt

def read_las_file(file_path):
    """读取 .las 文件并提取点云数据"""
    las_data = laspy.read(file_path)
    x = las_data.x
    y = las_data.y
    z = las_data.z
    intensity = las_data.intensity  # 假设强度是第四个维度
    points = np.vstack((x, y, z, intensity)).transpose()
    return points

def remove_outliers(points):
    """删除 z 值在上下四分位之外的点"""
    z_values = points[:, 2]
    q1 = np.percentile(z_values, 25)
    q3 = np.percentile(z_values, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    filtered_points = points[(z_values >= lower_bound) & (z_values <= upper_bound)]
    return filtered_points

def save_filtered_points(file_path, points):
    """保存处理后的点云数据"""
    points.astype(np.float32).tofile(file_path)

def process_las_files(input_folder, output_folder):
    """处理文件夹中的所有 .las 文件"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".las"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename.replace(".las", ".bin"))
            
            # 读取 .las 文件
            points = read_las_file(input_file)
            
            # 提取 z 值并绘制箱线图
            z_values = points[:, 2]
            
            # 删除 z 值在上下四分位之外的点
            filtered_points = remove_outliers(points)
            
            # 保存处理后的点云数据
            save_filtered_points(output_file, filtered_points)
            
            print(f"已处理文件 {input_file} 并保存到 {output_file}")

if __name__ == "__main__":                                                              
    input_folder = '/root/autodl-fs/MapTR1/data/custom/test/las'  # 替换为你的 .las 文件夹路径
    output_folder = '/root/autodl-fs/MapTR1/data/custom/test/after_translated2'  # 替换为你的输出文件夹路径
    
    process_las_files(input_folder, output_folder)
