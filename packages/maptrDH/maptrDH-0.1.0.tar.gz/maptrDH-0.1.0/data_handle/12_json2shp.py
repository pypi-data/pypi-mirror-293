import geopandas as gpd
import os
folder_a=r'/root/autodl-fs/MapTR1/data/rest_noise'
folder_b=r'/root/autodl-fs/MapTR1/data/rest_shp'
for filename_a in os.listdir(folder_a):
        if filename_a.endswith(".json"):
            filename_b = filename_a.replace(".json", ".shp")
            file_path_a = os.path.join(folder_a, filename_a)
            file_path_b = os.path.join(folder_b, filename_b)
            # 从GeoJSON文件中读取数据
            gdf = gpd.read_file(file_path_a)

            # 将数据保存为Shapefile
            gdf.to_file(file_path_b, driver='ESRI Shapefile')
print("全部转换完毕！")
