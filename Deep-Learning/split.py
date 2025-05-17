import os
import shutil
from collections import defaultdict

def emotion_code_to_label(code):
    # Map mã emotion sang tên nhãn
    mapping = {
        '01': 'Neutral',
       
        '03': 'Happy',
        '04': 'Sad',
        '05': 'Angry',
        '06': 'Fear',
        '07': 'Disgust',
        '08': 'Surprise'
    }
    return mapping.get(code, None)

def split_ravdess_by_actor(root_dir, output_dir, train_actors, val_actors, test_actors, ignore_labels=['Calm']):
    # Tạo dict chứa file theo nhãn
    files_by_label = defaultdict(list)
    
    for file in os.listdir(root_dir):
        if not file.endswith('.wav'):
            continue
        
        parts = file.split('-')
        emotion_code = parts[2]  # tiền tố thứ 3 (0-based index)
        actor_id = parts[6].split('.')[0]  # tiền tố thứ 7, bỏ đuôi .wav
        
        label = emotion_code_to_label(emotion_code)
        if label is None or label in ignore_labels:
            continue
        
        files_by_label[label].append((file, actor_id))
    
    # Hàm copy file theo actor list vào folder tương ứng
    def copy_files(file_list, split_name):
        for label, files in file_list.items():
            for file, actor in files:
                if actor in actor_lists[split_name]:
                    src = os.path.join(root_dir, file)
                    dst_dir = os.path.join(output_dir, split_name, label)
                    os.makedirs(dst_dir, exist_ok=True)
                    shutil.copy(src, dst_dir)
    
    # Actor phân theo tập Train, Val, Test
    actor_lists = {
        'Train-RAVDESS': train_actors,
        'Val-RAVDESS': val_actors,
        'Test-RAVDESS': test_actors
    }
    
    # Chuẩn bị dict chứa file phân chia theo split
    split_files = {
        'Train-RAVDESS': defaultdict(list),
        'Val-RAVDESS': defaultdict(list),
        'Test-RAVDESS': defaultdict(list)
    }
    
    # Phân loại file theo actor list cho từng split
    for label, files in files_by_label.items():
        for file, actor in files:
            if actor in actor_lists['Train-RAVDESS']:
                split_files['Train-RAVDESS'][label].append((file, actor))
            elif actor in actor_lists['Val-RAVDESS']:
                split_files['Val-RAVDESS'][label].append((file, actor))
            elif actor in actor_lists['Test-RAVDESS']:
                split_files['Test-RAVDESS'][label].append((file, actor))
    
    # Copy file vào thư mục tương ứng
    for split_name in ['Train-RAVDESS', 'Val-RAVDESS', 'Test-RAVDESS']:
        copy_files(split_files[split_name], split_name)

# Ví dụ:
root_dir = 'Dataset/ALL'
output_dir = 'Dataset/RAVDESS_split'

# Chia actor theo tập train, val, test (ví dụ actor ID từ 01 đến 24)
train_actors = [f'{i:02d}' for i in range(1, 17)]  # actor 01-16
val_actors = [f'{i:02d}' for i in range(17, 20)]   # actor 17-19
test_actors = [f'{i:02d}' for i in range(20, 25)]  # actor 20-24

split_ravdess_by_actor(root_dir, output_dir, train_actors, val_actors, test_actors)
