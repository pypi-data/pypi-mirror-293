import os
import json
import numpy as np

# 给定的范围
min_bounds = np.array([-19.735,-19.677])
max_bounds = np.array([19.735, 19.677])

def is_out_of_bounds(coord, min_bounds, max_bounds):
    """检查坐标是否超出给定的范围"""
    return np.any(coord < min_bounds) or np.any(coord > max_bounds)

def check_and_delete_files(folder_path, min_bounds, max_bounds):
    out_of_bounds_files = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # 提取所有坐标
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
            
            # 检查坐标是否超出范围
            out_of_bounds = False
            for coord in coordinates:
                if isinstance(coord[0], list):  # 处理多层嵌套的坐标
                    for inner_coord in coord:
                        if is_out_of_bounds(inner_coord[:2], min_bounds, max_bounds):
                            out_of_bounds = True
                            break
                else:
                    if is_out_of_bounds(coord[:2], min_bounds, max_bounds):
                        out_of_bounds = True
                        break
            
            if out_of_bounds:
                out_of_bounds_files.append(filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

    return out_of_bounds_files

folder_path = '/root/autodl-fs/MapTR1/data/custom/train_rotation/afterCutted_translated'
out_of_bounds_files = check_and_delete_files(folder_path, min_bounds, max_bounds)
print("Out-of-bounds files:", out_of_bounds_files)