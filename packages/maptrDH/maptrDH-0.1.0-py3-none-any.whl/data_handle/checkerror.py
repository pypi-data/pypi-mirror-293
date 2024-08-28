import os
import re

def find_non_continuous_files(folder):
    files = sorted(os.listdir(folder))
    pattern = re.compile(r'(\d{6})_(\d{4})_removeLimit\.bin')
    
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

def delete_files(folder, files):
    for file in files:
        file_path = os.path.join(folder, file)
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

folder = '/root/autodl-fs/MapTR1/data/custom/train_rotation/after_translated'
non_continuous_files = find_non_continuous_files(folder)
print("Non-continuous files:", non_continuous_files)

# Delete the non-continuous files
# delete_files(folder, non_continuous_files)
