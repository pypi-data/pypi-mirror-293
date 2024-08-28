import pickle as pkl
import pandas as pd
from shapely.geometry import LineString, MultiPoint
import pickle
import json

# 打开.pkl文件     '/root/autodl-fs/MapTR1/data/nuscenes/nuscenes_infos_temporal_train.pkl'
with open('/root/autodl-fs/MapTR1/data/custom/test/test_full_rotation.pkl', 'rb') as file:
    # 使用pickle.load()方法加载数据
    data_dict = pickle.load(file)
data_dict=data_dict['infos']
Classmapping = {'solid_divider': 0, 'dashed_divider': 1}
val_data={
    'GTs':[]
}
for Ddict in data_dict:
    token = Ddict['token']
    gt_labels = Ddict['ann_info']['gt_labels_3d']
    gt_instances =Ddict['ann_info']['gt_bboxes_3d']
    gt_vectors={
    'token':token,
    'vectors':[]
    }
    for label, instance in zip(gt_labels, gt_instances):
        # 将 LineString 转换为 Python 数组
        pts_array = list(instance.coords)
        pts_array = [list(tup) for tup in pts_array]
        vct = {
            'pts':pts_array,
            'pts_num':len(pts_array),
            'cls_name':label,
            'type':Classmapping[label]
        }
        gt_vectors['vectors'].append(vct)
    val_data['GTs'].append(gt_vectors)
# 将字典转换为 JSON 字符串
json_string = json.dumps(val_data)

# 将 JSON 字符串写入文件
with open("/root/autodl-fs/MapTR1/data/custom/test/test_full_rotation.json", "w") as json_file:                                
    json_file.write(json_string)
print("sucess !")
