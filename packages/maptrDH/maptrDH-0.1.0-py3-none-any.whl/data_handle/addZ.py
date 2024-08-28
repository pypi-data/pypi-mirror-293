import json
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon, MultiLineString

def read_geojson(file_path):
    """读取 GeoJSON 文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_z_value_to_geometry(geojson_data, z_value=5.8):
    """为 GeoJSON 数据中的几何体添加 Z 值"""
    features = geojson_data['features']
    geometries = []
    properties_list = []

    for feature in features:
        geometry = feature['geometry']
        properties = feature['properties']

        if geometry['type'] == 'Point':
            coords = geometry['coordinates']
            point = Point(coords[0], coords[1], z_value)
            geometries.append(point)
        
        elif geometry['type'] == 'LineString':
            coords = [(*coord, z_value) for coord in geometry['coordinates']]
            line = LineString(coords)
            geometries.append(line)
        
        elif geometry['type'] == 'Polygon':
            rings = []
            for ring in geometry['coordinates']:
                rings.append([(*coord, z_value) for coord in ring])
            polygon = Polygon(rings)
            geometries.append(polygon)
        
        elif geometry['type'] == 'MultiLineString':
            multilines = []
            for line in geometry['coordinates']:
                coords = [(*coord, z_value) for coord in line]
                multilines.append(LineString(coords))
            multi_line = MultiLineString(multilines)
            geometries.append(multi_line)
        
        properties_list.append(properties)

    return geometries, properties_list

def save_to_shapefile(geometries, properties_list, output_path, crs="EPSG:4326"):
    """将几何数据和属性保存为 Shapefile"""
    print(f"Geometries length: {len(geometries)}, Properties length: {len(properties_list)}")
    gdf = gpd.GeoDataFrame(properties_list, geometry=geometries)
    gdf.set_crs(crs, inplace=True)
    gdf.to_file(output_path)

if __name__ == "__main__":
    input_geojson = r'/root/autodl-fs/MapTR1/data/temp/shelter2.geojson'
    output_shp = r'/root/autodl-fs/MapTR1/data/temp/shelter2.shp'

    # 读取 GeoJSON 文件
    geojson_data = read_geojson(input_geojson)

    # 为几何体添加 Z 值
    geometries, properties_list = add_z_value_to_geometry(geojson_data)

    # 保存为 Shapefile
    save_to_shapefile(geometries, properties_list, output_shp)

    print(f"已将 GeoJSON 数据保存为 Shapefile: {output_shp}")
