import os
import shapefile
from shapely.geometry import Polygon, LineString
import json
from scipy.spatial import cKDTree
from shapely.geometry import shape
import numpy as np
import laspy
import math

class BBox:
    def __init__(self, p1, p2, p3, p4):
        """
        使用四个角点初始化 BBox。
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def is_inside(self, point):
        """
        检查给定点是否在 BBox 内部。
        """
        # 计算每个角点到给定点的向量
        v1 = (self.p1[0] - point[0], self.p1[1] - point[1])
        v2 = (self.p2[0] - point[0], self.p2[1] - point[1])
        v3 = (self.p3[0] - point[0], self.p3[1] - point[1])
        v4 = (self.p4[0] - point[0], self.p4[1] - point[1])

        # 计算相邻向量的叉乘
        cross1 = v1[0] * v2[1] - v1[1] * v2[0]
        cross2 = v2[0] * v3[1] - v2[1] * v3[0]
        cross3 = v3[0] * v4[1] - v3[1] * v4[0]
        cross4 = v4[0] * v1[1] - v4[1] * v1[0]

        # 检查叉乘是否具有相同的符号
        return (cross1 > 0 and cross2 > 0 and cross3 > 0 and cross4 > 0) or (cross1 < 0 and cross2 < 0 and cross3 < 0 and cross4 < 0)

    def is_line_inside(self, p1, p2):
        """
        检查给定线段是否完全在 BBox 内部。
        """
        return self.is_inside(p1) and self.is_inside(p2)

    def is_line_intersect(self, p1, p2):
        """
        检查给定线段是否与 BBox 相交。
        """
        # 检查线段是否与 BBox 的任一边相交
        edges = [(self.p1, self.p2), (self.p2, self.p3), (self.p3, self.p4), (self.p4, self.p1)]
        for edge in edges:
            if self.is_intersect(p1, p2, edge[0], edge[1]):
                return True
        
        return False

    def cross_product(self,A, B, C):
        """计算向量AC和向量AB的叉乘结果"""
        return (C[0] - A[0]) * (B[1] - A[1]) - (C[1] - A[1]) * (B[0] - A[0])

    def is_intersect(self,p1, p2, p3, p4):
        """判断线段p1p2和线段p3p4是否相交"""
        if (max(p1[0], p2[0]) >= min(p3[0], p4[0])  # 矩形相交
                and max(p3[0], p4[0]) >= min(p1[0], p2[0])
                and max(p1[1], p2[1]) >= min(p3[1], p4[1])
                and max(p3[1], p4[1]) >= min(p1[1], p2[1])):
            if (self.cross_product(p1, p2, p3) * self.cross_product(p1, p2, p4) <= 0
                    and self.cross_product(p3, p4, p1) * self.cross_product(p3, p4, p2) <= 0):
                return True
        return False

    def find_intersection(self,p1, p2, p3, p4):
        """如果线段相交，计算交点"""
        if not self.is_intersect(p1, p2, p3, p4):
            return 
        
        # 线段相交，计算交点
        x1 = p1[0]
        y1 = p1[1]
        x2 = p2[0]
        y2 = p2[1]
        x3, y3 = p3
        x4, y4 = p4
        
        # 解线性方程组
        denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if denominator == 0:
            return "线段重叠或平行，无法计算交点"
        
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
        # 交点坐标
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        
        return (x, y)

    def on_segment(self, p, q, r):
        """
        检查点 q 是否位于线段 pr 上。
        先检查 q 是否在由 p 和 r 形成的矩形内，然后检查 p, q, r 是否共线。
        """
        if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            # 检查共线性
            if self.cross_product(p, q, r) == 0:
                return True
        return False
    def is_bbox_inside(self, other_bbox):
        """
        检查另一个BBox是否完全在当前BBox内部。
        """
        # 检查other_bbox的所有顶点是否都在当前BBox内
        return all(self.is_inside(point) for point in [other_bbox.p1, other_bbox.p2, other_bbox.p3, other_bbox.p4])

def read_traj_file(file_path):
    points = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            coords = line.strip().split(',')
            x, y, z = map(float, coords)  # 将每行的坐标转换为浮点数
            points.append([x, y, z])
    return points

def find_intersection_points(feature, Bbox):
    intersection_Num=0
    coordinates = feature['geometry']['coordinates']
    intersection_points = []

    for i in range(len(coordinates)):
        point = coordinates[i]
        if i==len(coordinates)-1:
            next_point = point
        else:
            next_point = coordinates[i + 1]
        if Bbox.is_inside(point):
            intersection_points.append(point)
    
            if not Bbox.is_inside(next_point):
                Intersections = []
                edges = [(Bbox.p1, Bbox.p2), (Bbox.p2, Bbox.p3), (Bbox.p3, Bbox.p4), (Bbox.p4, Bbox.p1)]
                for edge in edges:
                    intersection = Bbox.find_intersection(point, next_point, *edge)
                    if intersection:
                        Intersections.append(intersection)
                intersection_Num+=len(Intersections)
                intersection_points.extend([point for point in Intersections])

        else:
             if Bbox.is_inside(next_point):
                Intersections = []
                edges = [(Bbox.p1, Bbox.p2), (Bbox.p2, Bbox.p3), (Bbox.p3, Bbox.p4), (Bbox.p4, Bbox.p1)]
                for edge in edges:
                    intersection = Bbox.find_intersection(point, next_point, *edge)
                    if intersection:
                        Intersections.append(intersection)
                intersection_Num+=len(Intersections)
                intersection_points.extend([point for point in Intersections])

    return intersection_points,intersection_Num

def update_feature_coordinates_with_z(features, tree, point_cloud_data):
    for feature in features:
        geometry = feature['geometry']
        new_coordinates = []
        
        if geometry['type'] == 'LineString':
            for xy in geometry['coordinates']:
                xy=[xy[0],xy[1]]
                # 使用cKDTree找到最近的点云点
                distance, index = tree.query(xy)
                # 获取对应的z坐标
                z = point_cloud_data[index][2]
                # 更新坐标，包含z值
                new_coordinates.append((xy[0], xy[1], float(z)))
                
            # 更新特征的几何体坐标
            feature['geometry']['coordinates'] = new_coordinates
    return features

def update_z(features):
    for feature in features:
        geometry = feature['geometry']
        new_coordinates = []
        
        if geometry['type'] == 'LineString':
            for xy in geometry['coordinates']:
                xy=[xy[0],xy[1]]
                # 更新坐标，包含z值
                new_coordinates.append((xy[0], xy[1], float(0)))
                
            # 更新特征的几何体坐标
            feature['geometry']['coordinates'] = new_coordinates
    return features

if __name__ == "__main__":
    LENGTH = 30.0
    WIDTH = 18.0
    # 读取GeoJSON文件
    with open('/root/autodl-fs/MapTR1/data/custom/GT_SHP/dashed_lane.shp-geo.json') as f:
        Sdata = json.load(f)

    # 指定保存GeoJSON文件的文件夹路径
    output_folder = '/autodl-fs/data/MapTR1/data/custom/train_0.3/afterCutted'
    output_folder_record='/root/autodl-fs/MapTR1/data/custom/train/record_new.json'

    # 指定点云文件所在的文件夹路径
    traj_folder = '/root/autodl-fs/MapTR1/data/custom/traj_0.3'   # .traj格式的          

    # 获取点云文件列表
    point_cloud_files = [os.path.join(traj_folder, file) for file in os.listdir(traj_folder) if file.endswith('.traj')]

    record_Num=[]

    # 遍历点云文件
    for index, point_cloud_file in enumerate(point_cloud_files):    
        file_name = point_cloud_file.split("/")[-1]
        filename_traj = file_name
        path_traj = os.path.join(traj_folder, filename_traj)
        traj_data = read_traj_file(path_traj)
        # 计算首末两个点的平均值以求中心点
        first_point = traj_data[0][:2]  # 只取x和y
        last_point = traj_data[-1][:2]  # 只取x和y

        # 使用列表推导式计算中心点坐标，只考虑x和y
        center_point = [(first_point[i] + last_point[i]) / 2 for i in range(len(first_point))]

        # 计算向量，只考虑x和y
        vector = [last_point[i] - first_point[i] for i in range(len(first_point))]

        # 向量长度
        length_vector = math.sqrt(sum([x**2 for x in vector]))

        # 单位向量
        unit_vector = [x / length_vector for x in vector]

        # 垂直单位向量，在二维空间
        perpendicular_vector = [-unit_vector[1], unit_vector[0]]

        # 计算bbox的四个顶点
        half_length = LENGTH / 2
        half_width = WIDTH / 2

        p1 = [center_point[0] + half_length * unit_vector[0] + half_width * perpendicular_vector[0],
            center_point[1] + half_length * unit_vector[1] + half_width * perpendicular_vector[1]]
        p2 = [center_point[0] - half_length * unit_vector[0] + half_width * perpendicular_vector[0],
            center_point[1] - half_length * unit_vector[1] + half_width * perpendicular_vector[1]]
        p3 = [center_point[0] - half_length * unit_vector[0] - half_width * perpendicular_vector[0],
            center_point[1] - half_length * unit_vector[1] - half_width * perpendicular_vector[1]]
        p4 = [center_point[0] + half_length * unit_vector[0] - half_width * perpendicular_vector[0],
            center_point[1] + half_length * unit_vector[1] - half_width * perpendicular_vector[1]]

        # 创建 BBox 对象
        bbox = BBox(p1, p2, p3, p4)

        file_name_parts = file_name.split(".")
        last_character = file_name_parts[0]
        # 创建一个新的GeoJSON对象
        new_geojson = {
            "type": "FeatureCollection",
            "features": []
        }

        # 获取features下每个几何对象的bbox
        for feature in Sdata['features']:
            geometry = shape(feature['geometry'])
            bbox_shp = geometry.bounds
            bbox_array = BBox([bbox_shp[0],bbox_shp[1]], [bbox_shp[0],bbox_shp[3]], [bbox_shp[2],bbox_shp[3]], [bbox_shp[2],bbox_shp[1]])
            
            # 判断当前bbox_array是否完全被包含于当前polygon_las
            if bbox.is_bbox_inside(bbox_array):
                # 如果是，将当前feature添加至new_geojson中
                new_geojson["features"].append(feature)
            else:
                coordinates,MaxNum=find_intersection_points(feature,bbox)
                if len(coordinates)==1:
                    print("aaa")
                if MaxNum==0:        # Listring为什么会只有一个点  'properties'                 
                    continue
                coordinates = [[float(coord[0]), float(coord[1])] for coord in coordinates]
                new_feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": feature['geometry']['type'],
                        "coordinates": coordinates    # '112233_0211'                                                                                                                   
                    },
                    "properties": feature['properties'],
                    'MaxNum':MaxNum
                }
                
                new_geojson['features'].append(new_feature)
        if len(new_geojson['features'])==0:
            record_Num.append(last_character)
        # 更新特征集
        updated_features = update_z(new_geojson['features'])

        # 将更新后的特征集保存回GeoJSON数据中
        new_geojson['features'] = updated_features
        # 保存新的GeoJSON文件
        output_file = os.path.join(output_folder, f'dashed_{last_character}.json')
        with open(output_file, 'w') as f:
            json.dump(new_geojson, f)
        print(index)
    re_json={
        'record_Num':record_Num
    }
    with open(output_folder_record, 'w') as f:
            json.dump(re_json, f)