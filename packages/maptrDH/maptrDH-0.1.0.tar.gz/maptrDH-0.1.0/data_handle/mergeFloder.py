import os
import json
def merge_geojson_files(input_folder, output_file):
    features = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.geojson') or filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
                features.extend(geojson_data['features'])

    # 创建合并后的 GeoJSON 对象
    merged_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # 将合并后的 GeoJSON 数据写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_geojson, f, ensure_ascii=False, indent=4)

    print(f"合并后的 GeoJSON 文件已保存到 {output_file}")
if __name__ == "__main__":
    input_folder = r'/root/autodl-fs/MapTR1/data/solid'  # 替换为你的 GeoJSON 文件夹路径
    output_file = r'/root/autodl-fs/MapTR1/data/solid/solid_GT.geojson'  # 替换为你的输出文件路径                 
    merge_geojson_files(input_folder, output_file)
