import numpy as np
import laspy
import open3d as o3d
import os
def pcd2las(file,save_path):
    pcd = o3d.io.read_point_cloud(file)
    points = np.asarray(pcd.points)

    colors = np.asarray(pcd.colors)

    # las = laspy.create(point_format=6, file_version="1.4")
    las = laspy.create(point_format=3, file_version="1.2")
    las.x = points[:, 0]
    las.y = points[:, 1]
    las.z = points[:, 2]

    las.red = colors[:, 0] * 255
    las.green = colors[:, 1] * 255
    las.blue = colors[:, 2] * 255

    las.write(save_path)


# 调用批量转换函数
input_folder = r'/autodl-fs/data/MapTR1/data/custom/test_of_test/pcd'
output_folder = r'/autodl-fs/data/MapTR1/data/custom/test_of_test/las'                                                               
for filename in os.listdir(input_folder):
    if filename.endswith('.pcd'):
        # 构建输入和输出文件的完整路径
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename.replace('.pcd', '.las'))
        pcd2las(input_file_path, output_file_path)

print("全部转换完成！")                                 
