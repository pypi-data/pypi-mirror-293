import os
import numpy as np
# import laspy
import numpy as np
import laspy
import open3d as o3d

def las_to_pcd(las_file, pcd_file):
    # 读取las文件
    inFile = laspy.read(las_file)
    
     # 获取点云数据
    points = np.vstack((inFile.x, inFile.y, inFile.z)).T  # 将x、y、z坐标堆叠成矩阵

    # 构建点云对象
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)  # 无需切片，直接赋值点云数据

    # 如果存在强度信息，则进行归一化处理并设置颜色
    if hasattr(inFile, 'intensity'):
        intensity = inFile.intensity.astype(np.float64)  # 将强度信息转换为浮点数类型                                                           
        if np.max(intensity) != 0:
            intensity /= np.max(intensity)
            pcd.colors = o3d.utility.Vector3dVector(np.vstack((intensity, intensity, intensity)).T)

    # 保存为pcd文件
    o3d.io.write_point_cloud(pcd_file, pcd)
    print("转换完成")


input_folder = r'/root/autodl-fs/MapTR1/data/custom/train_0.3/las'
output_folder = r'/root/autodl-fs/MapTR1/data/custom/train_0.3/pcd'

i=1
# Iterate over each .pcd file in the input folder                                                   
for filename in os.listdir(input_folder):
    if filename.endswith('.las'):
        print(i)
        i=i+1
        las_path = os.path.join(input_folder, filename)
        pcd_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.pcd')
        # 执行转换
        las_to_pcd(las_path, pcd_file)
       
print("end")