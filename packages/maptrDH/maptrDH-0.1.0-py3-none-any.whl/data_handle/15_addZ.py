# import pickle as pkl
# import pandas as pd

# import pickle

# # 打开.pkl文件
# with open('/root/autodl-fs/MapTR1/data/custom/val_data.pkl', 'rb') as file:
#     # 使用pickle.load()方法加载数据
#     data = pickle.load(file)

# with open(r'/root/autodl-fs/MapTR1/data/nuscenes/nuscenes_infos_temporal_val.pkl', "rb") as f:
# 	object = pkl.load(f,encoding='latin1')
# df = pd.DataFrame(object)
# df.to_csv(r'/root/autodl-fs/MapTR1/tools/newPATH.csv')
# print("a")

# import laspy
# import numpy as np

# # 读取 .las 文件
# las_file = laspy.read("your_file.las")

# # 获取点云数据
# points = np.vstack([las_file.x, las_file.y, las_file.z]).T

# # 计算点云的长宽
# min_x = np.min(points[:, 0])
# max_x = np.max(points[:, 0])
# min_y = np.min(points[:, 1])
# max_y = np.max(points[:, 1])

# # 计算长宽
# width = max_x - min_x
# height = max_y - min_y

# print("Width:", width)
# print("Height:", height)
import os
import json

def update_geojson_z_values(geojson_path, z_offset=0.1):
    """更新GeoJSON文件中的z坐标值，增加z_offset。"""
    # 读取GeoJSON文件
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    # 遍历GeoJSON中的所有特征
    for feature in geojson_data['features']:
        if 'geometry' in feature:
            geometry = feature['geometry']
            if geometry['type'] == 'Point':
                coords = geometry['coordinates']
                if len(coords) == 3:
                    coords[2] += z_offset
            elif geometry['type'] in ['MultiPoint', 'LineString']:
                for coords in geometry['coordinates']:
                    if len(coords) == 3:
                        coords[2] += z_offset
            elif geometry['type'] in ['MultiLineString', 'Polygon']:
                for line in geometry['coordinates']:
                    for coords in line:
                        if len(coords) == 3:
                            coords[2] += z_offset
            elif geometry['type'] == 'MultiPolygon':
                for polygon in geometry['coordinates']:
                    for line in polygon:
                        for coords in line:
                            if len(coords) == 3:
                                coords[2] += z_offset
    
    # 将更新后的GeoJSON写回文件
    with open(geojson_path, 'w') as f:
        json.dump(geojson_data, f, indent=4)
        print("yes")

input_folder='/root/autodl-fs/MapTR1/data/custom/result_0.05_without'
# 获取文件夹中的所有文件
files = os.listdir(input_folder)
i=0
for filename in files:
    if filename.endswith('.json'):
        path=os.path.join(input_folder, filename)
        i=i+1
        update_geojson_z_values(path,10)
        print(i)