import os
import re
import pickle
import geopandas as gpd

def find_non_continuous_files(folder):
    files = sorted(os.listdir(folder))
    pattern = re.compile(r'(\d{6})_(\d{4})\.bin')
    
    previous_number = None
    non_continuous_files = []
    
    for filename in files:
        match = pattern.match(filename)
        if match:
            base_number, sequence_number = match.groups()
            sequence_number = int(sequence_number)
            
            if previous_number is not None and sequence_number != previous_number + 1:
                non_continuous_files.append(filename)
            
            previous_number = sequence_number
    
    return non_continuous_files

GT_path = r'/root/autodl-fs/MapTR1/data/custom/test/removeDensity'
Lidar_folder_path = r'/root/autodl-fs/MapTR1/data/custom/test/after_translated'
dict_data = {'infos': []}

# 找到不连续的文件              
non_continuous_files = find_non_continuous_files(Lidar_folder_path)
non_continuous_set = set(non_continuous_files)  # 转换为集合以便快速查找

prev_lidarPath = None
# 使用 sorted 函数确保文件名按字典顺序排序
for filename in sorted(os.listdir(Lidar_folder_path)):
    if filename.endswith('.bin'):
        print(filename)
        dict_data_info = {
            'lidar_path': "", 'prev_lidarPath': '', 'token': '', 'gt_path': [],
            'ann_info': {
                'gt_labels_3d': [], 'gt_bboxes_3d': []
            }
        }
        file_path = os.path.join(Lidar_folder_path, filename)

        # 如果文件名在不连续文件列表中，则 prev_lidarPath 设置为 None           
        if filename in non_continuous_set:
            dict_data_info['prev_lidarPath'] = None
        else:
            dict_data_info['prev_lidarPath'] = prev_lidarPath if prev_lidarPath is not None else None

        prev_lidarPath = file_path

        if not os.path.exists(file_path):
            print("文件夹路径不存在")
            break
        dict_data_info['lidar_path'] = file_path
        file_name = os.path.splitext(filename)[0]  # 获取文件名（不包含扩展名）
        lidar_prefix = file_name.split('_')[0] + file_name.split('_')[1]  # 使用下划线分割文件名，并获取前两个部分
        dict_data_info['token'] = lidar_prefix

        for GT_filename in os.listdir(GT_path):
            if GT_filename.endswith('.json'):
                GT_file_path = os.path.join(GT_path, GT_filename)
                GT_filename = os.path.splitext(GT_filename)[0]  # 获取文件名（不包含扩展名）
                GT_prefix = GT_filename.split('_')[-2] + GT_filename.split('_')[-1]
                GT_class = GT_filename.split('_')[0]
                if GT_class == 'dashed':
                    if GT_prefix == lidar_prefix:
                        dict_data_info['gt_path'].append(GT_file_path)
                        data = gpd.read_file(GT_file_path)
                        for feature in data['geometry']:
                            dict_data_info['ann_info']['gt_labels_3d'].append('dashed_divider')
                            dict_data_info['ann_info']['gt_bboxes_3d'].append(feature)
                else:
                    if GT_prefix == lidar_prefix:
                        dict_data_info['gt_path'].append(GT_file_path)
                        try:
                            data = gpd.read_file(GT_file_path)
                        except Exception as e:
                            print(f"发生了异常：{GT_file_path}", e)
                        for feature in data['geometry']:
                            dict_data_info['ann_info']['gt_labels_3d'].append('solid_divider')
                            dict_data_info['ann_info']['gt_bboxes_3d'].append(feature)

        dict_data['infos'].append(dict_data_info)

with open("/root/autodl-fs/MapTR1/data/custom/test/test_full_rotation.pkl", 'wb') as fo:  # 将数据写入pkl文件       
    pickle.dump(dict_data, fo)

print(dict_data.keys())  # 测试我们读取的文件
