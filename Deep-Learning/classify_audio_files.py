import os
import shutil
from tqdm import tqdm

# Đường dẫn đến thư mục chứa các tệp âm thanh (input và output)
train_directory = 'Dataset/Train2'
output_directory = 'Dataset/Train3'

# Các nhãn tương ứng với các số trong phần thứ ba của tên tệp
emotion_labels = {
    '01': 'Neutral',
    '02': 'Calm',
    '03': 'Happy',
    '04': 'Sad',
    '05': 'angry',
    '06': 'Fear',
    '07': 'Surprise',
    '08': 'Disgust'
}

# Tạo thư mục gốc cho output nếu chưa tồn tại
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Tạo thư mục cho các nhãn trong thư mục output nếu chưa tồn tại
for label in emotion_labels.values():
    label_dir = os.path.join(output_directory, label)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

# Lấy danh sách tệp âm thanh
files = [f for f in os.listdir(train_directory) if f.endswith('.wav')]

# Hiển thị tiến trình sao chép
with tqdm(total=len(files), desc="Đang sao chép tệp", unit="tệp") as pbar:
    for file_name in files:
        # Lấy số thứ ba trong tên tệp (ví dụ '06' từ '03-01-06-01-02-01-12')
        label_number = file_name.split('-')[2]
        
        # Kiểm tra xem số thứ ba có trong các nhãn không
        if label_number in emotion_labels:
            # Lấy nhãn cảm xúc từ số thứ ba
            emotion = emotion_labels[label_number]
            # Sao chép tệp vào thư mục nhãn trong thư mục output
            source_path = os.path.join(train_directory, file_name)
            dest_path = os.path.join(output_directory, emotion, file_name)
            shutil.copy(source_path, dest_path)
        
        # Cập nhật tiến trình
        pbar.update(1)

print("Tệp âm thanh đã được sao chép và phân loại thành công vào thư mục train3.")
