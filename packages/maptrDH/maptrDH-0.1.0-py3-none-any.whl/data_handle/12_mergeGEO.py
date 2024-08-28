from shapely.geometry import LineString, mapping
import json
import os
import numpy as np

def extract_number(filename):
    return int(''.join(filter(str.isdigit, filename)))

def load_geojson(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_geojson(data, path):
    with open(path, 'w') as file:
        json.dump(data, file)

def is_close(point1, point2, threshold=1.99):
    """Check if two 3D points are close enough."""
    return np.linalg.norm(np.array(point1) - np.array(point2)) <= threshold

def merge_points(point1, point2):
    """Merge two 3D points into their midpoint and ensure the result is a list."""
    # Assumes that both points have three coordinates: x, y, z
    return [
        (point1[0] + point2[0]) / 2,
        (point1[1] + point2[1]) / 2,
        (point1[2] + point2[2]) / 2
    ]


def process_files(folder_path):
    files = sorted((os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')), key=extract_number)
    final_features = []
    prev_geojson = None
    globalID=0
    for i in range(len(files) - 1):
        current_file = files[i]
        next_file = files[i + 1]
        current_geojson = load_geojson(current_file) if not prev_geojson else prev_geojson
        next_geojson = load_geojson(next_file)

        current_features = current_geojson['features']
        next_features = next_geojson['features']

        for current_feature in current_features:
            new_point_list=[]
            merged = False
            if current_feature['geometry']['type'] == 'LineString':
                current_line = LineString(current_feature['geometry']['coordinates'])
                current_coords = list(current_line.coords[-3:])
                
                for next_feature in next_features:
                    if next_feature['geometry']['type'] == 'LineString':
                        next_line = LineString(next_feature['geometry']['coordinates'])
                        next_coords = list(next_line.coords[:3])
                        for cur_pt in current_coords:
                            for nxt_pt in next_coords:
                                if is_close(cur_pt, nxt_pt):
                                    new_point = merge_points(cur_pt, nxt_pt)
                                    new_point_list.append(new_point)
                                    current_coords.remove(cur_pt)
                                    next_coords.remove(nxt_pt)
                                    break
                                    # Update coordinates, converting tuple to list if necessary
                        if new_point_list != []:
                            updated_coords = [list(pt) for pt in current_line.coords[:-3]] + current_coords + new_point_list + next_coords + [list(pt) for pt in next_line.coords[3:]]
                            merged_line = LineString(updated_coords)
                            next_feature['geometry']['coordinates'] = list(merged_line.coords)
                            # next_feature['properties']['feature_index']=globalID
                            globalID +=1
                            current_features.remove(current_feature)
                            break
                # current_feature['properties']['feature_index']=globalID
                globalID +=1
        final_features.extend(current_features)
        prev_geojson = next_geojson

    final_features.extend(next_geojson['features'])  # Add remaining features from the last file                    
    merged_geojson = {
        "type": "FeatureCollection",
        "features": final_features
    }
    save_geojson(merged_geojson, os.path.join(folder_path, 'dash0.geojson'))


# Example usage
folder_path = '/root/autodl-fs/MapTR1/data/custom/result_0.05_without/dash'
process_files(folder_path)