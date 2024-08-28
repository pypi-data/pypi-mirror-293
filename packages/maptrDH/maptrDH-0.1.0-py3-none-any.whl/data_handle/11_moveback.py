import numpy as np
import os
import geopandas as gpd
import json

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
 
Out_path=r'/root/autodl-fs/MapTR1/data/custom/test/after_translated'
Lidar_folder_path=r'/root/autodl-fs/MapTR1/data/custom/test/bin'
Shp_Out_path=r'/root/autodl-fs/MapTR1/data/custom/temp/moveback'
Shp_folder_path=r'/root/autodl-fs/MapTR1/data/custom/temp'
# Out_path=r'/root/autodl-fs/MapTR1/data/custom/train/after_translated'
# Lidar_folder_path=r"/autodl-fs/data/MapTR1/data/custom/try_RL/bin"         # .bin格式                
# Shp_Out_path=r'/root/autodl-fs/MapTR1/data/custom/result_0.2_without/move'
# Shp_folder_path=r'/root/autodl-fs/MapTR1/data/custom/result_0.2_without'
# 遍历文件夹中的所有文件
# 获取两个文件夹中的文件列表
Shp_files = os.listdir(Shp_folder_path)
Lidar_files = os.listdir(Lidar_folder_path)
i=0
translation_vector=[]
# 假设Lidar_files是一个包含所有Lidar文件名的列表
for Lidarfilename in Lidar_files:
    if Lidarfilename.endswith('.bin'):
        file_path = os.path.join(Lidar_folder_path, Lidarfilename)
        # 检查文件夹路径是否存在
        if not os.path.exists(file_path):
            print("文件夹路径不存在")
            break
        # 读取 .bin 文件
        point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)  # 假设每个点有四个值：x, y, z, intensity
        # 计算点云的边界框
        bbox_min = np.min(point_cloud[:, :3], axis=0)
        bbox_max = np.max(point_cloud[:, :3], axis=0)
        bbox_center = (bbox_min + bbox_max) / 2

        # 计算平移量
        translation_vector = -bbox_center
        # # 对点云进行平移操作
        # point_cloud[:, :3] += translation_vector

        # # 保存平移后的点云到新的 .bin 文件
        # output_file_path = os.path.join(Out_path, Lidarfilename)
        # point_cloud.astype(np.float32).tofile(output_file_path)
        # i+=1
        print("点云",i)
    for Shpfilename in Shp_files:
        # 假设其他部分不变，仅展示修正的GeoJSON坐标平移部分
        if Shpfilename.endswith('.json'):
            number1 = extract_number(Shpfilename)
            number2 = extract_number(Lidarfilename)
            if number1 == number2:
                # 读取和修改JSON文件
                shpfile_path = os.path.join(Shp_folder_path, Shpfilename)
                with open(shpfile_path, "r") as f:
                    data = json.load(f)
                for feature in data["features"]:
                    geometry = feature["geometry"]
                    # 对每种几何类型进行适当的坐标遍历和平移操作
                    if geometry["type"] == "Point":
                        geometry["coordinates"][0] += translation_vector[0]
                        geometry["coordinates"][1] += translation_vector[1]
                    elif geometry["type"] == "LineString":
                        geometry["coordinates"] = [[x - translation_vector[0], y - translation_vector[1]] for x, y in geometry["coordinates"]]
                    elif geometry["type"] == "Polygon":
                        geometry["coordinates"] = [[[x + translation_vector[0], y + translation_vector[1]] for x, y in part] for part in geometry["coordinates"]]
                    elif geometry["type"] == "MultiPolygon":
                        geometry["coordinates"] = [[[[x + translation_vector[0], y + translation_vector[1]] for x, y in ring] for ring in part] for part in geometry["coordinates"]]

                # 保存修改后的GeoJSON文件
                shpoutput_file_path = os.path.join(Shp_Out_path, Shpfilename.replace("geojson", "json"))
                with open(shpoutput_file_path, "w") as f:
                    json.dump(data, f)
                print("矢量", i)

# Out_path=r'/root/autodl-fs/MapTR1/data/custom/train_translated'
# Lidar_folder_path=r'/root/autodl-fs/MapTR1/data/custom/try'
# Shp_Out_path=r'/root/autodl-fs/MapTR1/data/custom/result/result_shp'          
# Shp_folder_path=r'/root/autodl-fs/MapTR1/data/custom/result'          
# # 遍历文件夹中的所有文件
# # 获取两个文件夹中的文件列表
# Shp_files = os.listdir(Shp_folder_path)
# Lidar_files = os.listdir(Lidar_folder_path)
# i=0
# translation_vector=[]
# for Lidarfilename in Lidar_files:
#     if Lidarfilename.endswith('.bin'):
#         file_path = os.path.join(Lidar_folder_path, Lidarfilename)
#         # 检查文件夹路径是否存在
#         if not os.path.exists(file_path):
#             print("文件夹路径不存在")
#             break
#         # 读取 .bin 文件
#         point_cloud = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)  # 假设每个点有四个值：x, y, z, intensity
#         # 计算点云的边界框
#         bbox_min = np.min(point_cloud[:, :2], axis=0)
#         bbox_max = np.max(point_cloud[:, :2], axis=0)
#         bbox_center = (bbox_min + bbox_max) / 2

#         # 计算平移量
#         translation_vector = -bbox_center
#         # 对点云进行平移操作
#         # point_cloud[:, :2] += translation_vector

#         # 保存平移后的点云到新的 .bin 文件
#         # output_file_path = os.path.join(Out_path, Lidarfilename)
#         # point_cloud.astype(np.float32).tofile(output_file_path)
#         i+=1
#         print("点云",i)
#     for Shpfilename in Shp_files:
#         if Shpfilename.endswith('.geojson'):
#             number1 = extract_number(Shpfilename)
#             number2 = extract_number(Lidarfilename)
#             if number1==number2:
#                 # 读取 JSON 文件
#                 shpfile_path = os.path.join(Shp_folder_path, Shpfilename)
#                 with open(shpfile_path, "r") as f:
#                     data = json.load(f)
#                 for feature in data["features"]:
#                     geometry = feature["geometry"]
#                     if geometry["type"] == "Point":
#                         coordinates = geometry["coordinates"]
#                         coordinates[0] += translation_vector[0]
#                         coordinates[1] += translation_vector[1]
#                     elif geometry["type"] == "Polygon" or geometry["type"] == "MultiPolygon" or geometry["type"] == "LineString":
#                         for part in geometry["coordinates"]:
#                                 part[0] -= translation_vector[0]
#                                 part[1] -= translation_vector[1]
#                 shpoutput_file_path = os.path.join(Shp_Out_path, Shpfilename)
#                 with open(shpoutput_file_path, "w") as f:
#                     json.dump(data, f)
#                 print("矢量",i)

