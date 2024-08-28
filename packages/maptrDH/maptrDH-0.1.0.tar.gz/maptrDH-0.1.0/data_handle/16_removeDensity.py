import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import os

# 读取点云数据
def load_point_cloud(bin_file):
    point_cloud = np.fromfile(bin_file, dtype=np.float32).reshape(-1, 4) # Assuming x, y, z, intensity
    return point_cloud[:, :3]  # x, y, z

# 读取 GeoJSON 矢量数据
def load_geojson(geojson_file):
    return gpd.read_file(geojson_file)

# 创建缓冲区并计算点云密度
def check_line_density(line, point_cloud, buffer_distance=0.2, min_density=10):
    buffer = line.buffer(buffer_distance)
    points_within_buffer = point_cloud[
        np.array([buffer.contains(Point(p)) for p in point_cloud[:, :2]])
    ]
    density = len(points_within_buffer) / buffer.area
    return density >= min_density

# 处理文件夹中的对应文件
def process_geojson(point_cloud_dir, geojson_dir, output_dir, buffer_distance=0.2, min_density=10):
    # 获取矢量文件夹中的所有文件
    geojson_files = [f for f in os.listdir(geojson_dir) if f.endswith('.json')]
    i=0
    for geojson_file in geojson_files:
        # 如果发现文件夹/autodl-fs/data/MapTR1/data/custom/train_rotation/removeDensity中存在同名文件则跳过当前for循环  
        # 提取编号部分（假设编号格式为：112233_0030）
        base_name = "_".join(geojson_file.split('_')[1:]).split('.')[0]  # 提取112233_0030部分
        bin_file = f"{base_name}.bin"
        bin_path = os.path.join(point_cloud_dir, bin_file)
        # 构造输出文件的完整路径  
        output_file_path = os.path.join(output_dir, geojson_file)  
  
        # 检查输出文件是否已存在  
        if os.path.exists(output_file_path):  
            print(f"Skipping {output_file_path} because it already exists.")  
            continue  # 跳过当前循环  
        if os.path.exists(bin_path):
            process_single_file(bin_path, os.path.join(geojson_dir, geojson_file), output_dir, buffer_distance, min_density)

def process_single_file(point_cloud_file, geojson_file, output_dir, buffer_distance=0.2, min_density=10):
    point_cloud = load_point_cloud(point_cloud_file)
    geojson_data = load_geojson(geojson_file)

    filtered_features = []
    for _, feature in geojson_data.iterrows():
        line = feature.geometry
        if check_line_density(line, point_cloud, buffer_distance, min_density):
            filtered_features.append(feature)

    # 构建输出文件路径
    output_file = os.path.join(output_dir, os.path.basename(geojson_file))

    # 保存结果
    if filtered_features:
        filtered_geojson = gpd.GeoDataFrame(filtered_features)
        filtered_geojson.to_file(output_file, driver='GeoJSON')
        print(output_file)

# 执行处理
process_geojson(r"/root/autodl-fs/MapTR1/data/custom/train_rotation/after_translated", r"/root/autodl-fs/MapTR1/data/custom/train_rotation/afterCutted_translated", r"/root/autodl-fs/MapTR1/data/custom/train_rotation/removeDensity")
