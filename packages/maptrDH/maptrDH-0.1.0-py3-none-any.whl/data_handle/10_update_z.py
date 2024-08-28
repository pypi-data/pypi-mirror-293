# import os
# import shapefile
# from shapely.geometry import Polygon, LineString
# import json
# from scipy.spatial import cKDTree
# from shapely.geometry import shape
# import numpy as np
# import laspy
# import math

# def update_feature_coordinates_with_z(features, tree, point_cloud_data):
#     for feature in features:
#         geometry = feature['geometry']
#         new_coordinates = []
        
#         if geometry['type'] == 'LineString':
#             for xy in geometry['coordinates']:
#                 # 使用cKDTree找到最近的点云点
#                 distance, index = tree.query(xy)
#                 # 获取对应的z坐标
#                 z = point_cloud_data[index][2]
#                 # 更新坐标，包含z值
#                 new_coordinates.append((xy[0], xy[1], float(z)))
                
#             # 更新特征的几何体坐标
#             feature['geometry']['coordinates'] = new_coordinates
#     return features

# if __name__ == "__main__":
#     # 指定点云文件所在的文件夹路径
#     point_cloud_folder = '/root/autodl-fs/MapTR1/data/custom/try_RL/bin'   # .bin格式的          
#     shp_floder = '/autodl-fs/data/MapTR1/data/custom/result_0.2_without/move'           
#     # 获取点云文件列表
#     shp_files = [os.path.join(shp_floder, file) for file in os.listdir(shp_floder) if file.endswith('.geojson')]

#     # 遍历点云文件
#     for index, shp_file in enumerate(shp_files):    
#         lidar_file_path = os.path.join(point_cloud_folder, shp_file.replace('_removeLimit_shp.geojson', '_new.bin'))
#         # 假设point_cloud_data是从.bin文件加载的点云数据
#         point_cloud_data = np.fromfile(lidar_file_path, dtype=np.float32).reshape(-1, 4)

#         # 创建cKDTree索引，只使用点云数据的x和y坐标
#         tree = cKDTree(point_cloud_data[:, :2])

#         # 更新特征集
#         updated_features = update_feature_coordinates_with_z(new_geojson['features'], tree, point_cloud_data)



import os
import json
import numpy as np
from scipy.spatial import cKDTree

def load_bin_file(bin_path):
    """加载.bin文件并返回其点云数据。假设每个点由连续的x, y, z坐标组成。"""
    points = np.fromfile(bin_path, dtype=np.float32)
    return points.reshape(-1, 4)

def update_geojson_with_z(geojson_path, bin_path):
    """更新GeoJSON文件中的点，添加来自.bin文件的z坐标。"""
    # 读取GeoJSON文件
    with open(geojson_path, 'r') as f:
        geojson_data = json.load(f)
    
    # 从.bin文件加载点云并创建cKDTree
    point_cloud = load_bin_file(bin_path)
    tree = cKDTree(point_cloud[:, :2])  # 使用x, y坐标构建树
    
    for feature in geojson_data['features']:
        if 'geometry' in feature and feature['geometry']['type'] == 'LineString':
            updated_coords = []
            for xy in feature['geometry']['coordinates']:
                if len(xy)==3:
                    xy=xy[:2]
                _, idx = tree.query(xy, k=1)
                z = float(point_cloud[idx, 2])  # 转换为Python的float类型
                updated_coords.append([xy[0], xy[1], z + 0.2])
            feature['geometry']['coordinates'] = updated_coords
    file_name = os.path.basename(geojson_path) 
    geojson_path=r'/root/autodl-fs/MapTR1/data/custom/test/temp'#########!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    full_path = os.path.join(geojson_path, file_name) 
    # 将更新后的GeoJSON写回文件
    with open(full_path, 'w') as f:
        json.dump(geojson_data, f)

def process_folder(geojson_folder, bin_folder):
    """处理文件夹中的所有GeoJSON文件，为它们添加z坐标。"""
    for filename in os.listdir(geojson_folder):
        if filename.endswith('.json'):
            geojson_path = os.path.join(geojson_folder, filename)
            if 'dash' in filename:
                filename=filename.replace('dashed_1', '1')
            else:
                filename=filename.replace('solid_1', '1')
            bin_path = os.path.join(bin_folder, filename.replace('.json', '_new.bin'))
            if os.path.exists(bin_path):
                update_geojson_with_z(geojson_path, bin_path)
            else:
                print(f"No matching .bin file for {filename}")
        print(filename)
# 示例用法
point_cloud_folder = '/root/autodl-fs/MapTR1/data/custom/test/bin'   # .bin格式的          
shp_floder = '/root/autodl-fs/MapTR1/data/custom/test/afterCutted_translated' 
# geojson_folder = '/path/to/geojson_folder'
# bin_folder = '/path/to/bin_folder'
process_folder(shp_floder, point_cloud_folder)




