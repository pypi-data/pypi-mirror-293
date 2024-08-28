import shapefile
import json
import codecs
from tqdm import tqdm
import datetime

def Shp2JSON(filename, shp_encoding='utf-8', json_encoding='utf-8'):
    '''
    这个函数用于将shp文件转换为GeoJSON文件，保留Z坐标信息
    :param filename: shp文件对应的文件名（去除文件拓展名）
    :param shp_encoding: shapefile的编码
    :param json_encoding: 输出JSON文件的编码
    :return: None
    '''

    '''创建shp IO连接'''
    reader = shapefile.Reader(filename, encoding=shp_encoding)

    '''提取所有field部分内容'''
    fields = reader.fields[1:]

    '''提取所有field的名称'''
    field_names = [field[0] for field in fields]

    '''初始化要素列表'''
    buffer = []

    def default(obj):
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')  # 将日期对象转换为字符串
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    for sr in tqdm(reader.shapeRecords()):
        '''提取每一个矢量对象对应的属性值'''
        record = sr.record

        '''属性转换为列表'''
        record = [r.decode('gb2312', 'ignore') if isinstance(r, bytes)
                  else r for r in record]

        '''对齐属性与对应数值的键值对'''
        atr = dict(zip(field_names, record))

        '''获取当前矢量对象的类型及矢量信息，包括Z坐标'''
        geom = sr.shape.__geo_interface__

        '''确保Z坐标存在并加入geometry'''
        if 'coordinates' in geom and isinstance(geom['coordinates'][0], (list, tuple)):
            def add_z_coordinate(coords):
                '''递归处理嵌套的坐标，确保Z坐标存在'''
                if isinstance(coords[0], (list, tuple)):
                    return [add_z_coordinate(c) for c in coords]
                return coords + (0.0,) if len(coords) == 2 else coords

            geom['coordinates'] = add_z_coordinate(geom['coordinates'])

        '''向要素列表追加新对象'''
        buffer.append(dict(type="Feature",
                           geometry=geom,
                           properties=atr))

    '''写出GeoJSON文件'''
    with codecs.open(filename + "-withZ.json", "w", encoding=json_encoding) as geojson:
        json.dump({"type": "FeatureCollection", "features": buffer}, geojson, default=default)

    print('转换成功！')


if __name__ == '__main__':
    import os

    os.chdir(r'/root/autodl-fs/MapTR1/data/custom/GT_SHP')
    Shp2JSON(filename='dashed_lane',
             shp_encoding='gbk',
             json_encoding='utf-8')

    # import pickle

    # F = open(r'/root/autodl-fs/MapTR1/data/nuscenes/nuscenes_infos_temporal_train.pkl', 'rb')

    # content = pickle.load(F)
    # print("a")
    # # 创建一个Python对象
    # data = {
    #     'info':[{
    #         'lidar_path':'./data',
    #     },

    #     ]
    # }

    # # 将对象序列化为pkl文件
    # with open('data.pkl', 'wb') as file:
    #     pickle.dump(data, file)
    #######
    # import json
    # from shapely.geometry import shape

    # # 读取 GeoJSON 文件
    # with open('/root/autodl-fs/MapTR1/data/custom/GT_SHP/dashed_lane.shp-geo.json') as f:
    #     data = json.load(f)

    # # 获取第一条线的几何对象
    # line_geometry = data['features'][0]['geometry']

    # # 将线几何对象转换为 Shapely 的 LineString 对象
    # line = shape(line_geometry)

    # # 打印 LineString 对象
    # print(line)
