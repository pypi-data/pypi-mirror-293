import os
import numpy as np

def get_min_max_xyz(folder):
    # 初始化最小值和最大值
    min_x, min_y, min_z, min_i = float('inf'), float('inf'), float('inf'), float('inf')
    max_x, max_y, max_z, max_i = float('-inf'), float('-inf'), float('-inf'), float('-inf')
    
    # 初始化记录最值所在文件名的变量
    min_x_file, min_y_file, min_z_file, min_i_file = None, None, None, None
    max_x_file, max_y_file, max_z_file, max_i_file = None, None, None, None

    # 遍历文件夹中的所有 .bin 文件                          
    for filename in os.listdir(folder):
        if filename.endswith(".bin"):
            file_path = os.path.join(folder, filename)
            
            # 读取点云数据
            points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)

            # 更新最小值和最大值
            file_min_x = np.min(points[:, 0])
            file_min_y = np.min(points[:, 1])
            file_min_z = np.min(points[:, 2])
            file_min_i = np.min(points[:, 3])

            file_max_x = np.max(points[:, 0])
            file_max_y = np.max(points[:, 1])
            file_max_z = np.max(points[:, 2])
            file_max_i = np.max(points[:, 3])

            # 更新全局最小值和最小值文件
            if file_min_x < min_x:
                min_x = file_min_x
                min_x_file = filename
            if file_min_y < min_y:
                min_y = file_min_y
                min_y_file = filename
            if file_min_z < min_z:
                min_z = file_min_z
                min_z_file = filename
            if file_min_i < min_i:
                min_i = file_min_i
                min_i_file = filename

            # 更新全局最大值和最大值文件
            if file_max_x > max_x:
                max_x = file_max_x
                max_x_file = filename
            if file_max_y > max_y:
                max_y = file_max_y
                max_y_file = filename
            if file_max_z > max_z:
                max_z = file_max_z
                max_z_file = filename
            if file_max_i > max_i:
                max_i = file_max_i
                max_i_file = filename

    return (
        (min_x, min_y, min_z, min_i), (max_x, max_y, max_z, max_i),
        min_x_file, min_y_file, min_z_file, min_i_file,
        max_x_file, max_y_file, max_z_file, max_i_file
    )

if __name__ == "__main__":
    folder = '/root/autodl-fs/MapTR1/data/custom/test_0.3/after_translated'  # 替换为你的文件夹路径        

    # min_xyz, max_xyz, min_x_file, min_y_file, min_z_file, min_i_file,max_x_file, max_y_file, max_z_file, max_i_file = get_min_max_xyz(folder)            
    # print("最小值 (x, y, z, i):", min_xyz)
    # print("最大值 (x, y, z, i):", max_xyz)
    # print("x 最小值所属的文件:", min_x_file)
    # print("x 最大值所属的文件:", max_x_file)
    # print("y 最小值所属的文件:", min_y_file)
    # print("y 最大值所属的文件:", max_y_file)
    # print("z 最小值所属的文件:", min_z_file)
    # print("z 最大值所属的文件:", max_z_file) 

import os
import json

folder_path = '/root/autodl-fs/MapTR1/data/custom/test_0.3/afterCutted_translated'                          

# 初始化最小和最大值                
min_x = float('inf')
max_x = float('-inf')
min_y = float('inf')
max_y = float('-inf')

# 用于保存达到最值时的文件名                    
min_x_file = ""
max_x_file = ""
min_y_file = ""
max_y_file = ""

# 遍历文件夹中的所有geojson文件
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        # 读取geojson文件
        with open(os.path.join(folder_path, filename), 'r') as f:
            data = json.load(f)
        
        # 提取坐标信息
        coordinates = []
        if 'features' in data:
            for feature in data['features']:
                if 'geometry' in feature and 'coordinates' in feature['geometry']:
                    coords = feature['geometry']['coordinates']
                    # 处理可能的嵌套坐标列表
                    if isinstance(coords[0][0], list):
                        for sublist in coords:
                            coordinates.extend(sublist)
                    elif isinstance(coords[0], list):
                        coordinates.extend(coords)
                    else:
                        coordinates.append(coords)
        
        # 计算xy最值，并记录文件名
        for coord in coordinates:
            # 假设coord可能是多层嵌套的列表，我们需要的是最内层的x,y坐标
            if isinstance(coord[0], list):  # 处理多边形等多层嵌套坐标的情况
                for inner_coord in coord:
                    x, y = inner_coord[0], inner_coord[1]
                    if x < min_x:
                        min_x, min_x_file = x, filename
                    if x > max_x:
                        max_x, max_x_file = x, filename
                    if y < min_y:
                        min_y, min_y_file = y, filename
                    if y > max_y:
                        max_y, max_y_file = y, filename
            else:
                x, y = coord
                if x < min_x:
                    min_x, min_x_file = x, filename
                if x > max_x:
                    max_x, max_x_file = x, filename
                if y < min_y:
                    min_y, min_y_file = y, filename
                if y > max_y:
                    max_y, max_y_file = y, filename

# 输出最值及其对应的文件名
print(f"min_x: {min_x}, in file: {min_x_file}")
print(f"max_x: {max_x}, in file: {max_x_file}")
print(f"min_y: {min_y}, in file: {min_y_file}")
print(f"max_y: {max_y}, in file: {max_y_file}")
