import os
from collections import Counter

def get_ravdess_labels(dataset_path):
    """
    Trả về dict: {actor_folder: [danh sách nhãn xuất hiện]}
    - dataset_path: đường dẫn thư mục RAVDESS gốc
    - Nhãn là tiền tố thứ 3 trong tên file (theo chuẩn RAVDESS)
    """
    actor_labels = {}
    for actor in sorted(os.listdir(dataset_path)):
        actor_path = os.path.join(dataset_path, actor)
        if not os.path.isdir(actor_path):
            continue
        labels = set()
        for fname in os.listdir(actor_path):
            if fname.endswith('.wav'):
                parts = fname.split('-')
                if len(parts) > 2:
                    labels.add(parts[2])
        actor_labels[actor] = sorted(labels)
    return actor_labels

def get_ravdess_label_counts(dataset_path):
    """
    Trả về dict: {actor_folder: Counter({label: count, ...})}
    - dataset_path: đường dẫn thư mục RAVDESS gốc
    - Nhãn là tiền tố thứ 3 trong tên file (theo chuẩn RAVDESS)
    """
    actor_label_counts = {}
    for actor in sorted(os.listdir(dataset_path)):
        actor_path = os.path.join(dataset_path, actor)
        if not os.path.isdir(actor_path):
            continue
        label_counter = Counter()
        for fname in os.listdir(actor_path):
            if fname.endswith('.wav'):
                parts = fname.split('-')
                if len(parts) > 2:
                    label_counter[parts[2]] += 1
        actor_label_counts[actor] = dict(label_counter)
    return actor_label_counts

# Ví dụ sử dụng:
if __name__ == "__main__":
    dataset_path = "/content/drive/MyDrive/Colab Notebooks/Dataset/RAVDESS"
    labels_dict = get_ravdess_labels(dataset_path)
    for actor, labels in labels_dict.items():
        print(f"{actor}: {labels}")

    label_counts = get_ravdess_label_counts(dataset_path)
    for actor, label_count in label_counts.items():
        print(f"{actor}:")
        for label, count in sorted(label_count.items()):
            print(f"  Nhãn {label}: {count} file")