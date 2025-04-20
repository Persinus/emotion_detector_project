# emotion_detector_project

## Mô tả dự án
Dự án này sử dụng mô hình học sâu (CNN) để nhận diện cảm xúc từ ảnh. Mô hình được huấn luyện với bộ dữ liệu cảm xúc từ ảnh như FER2013. Dự án này gồm các bước từ xử lý dữ liệu, xây dựng và huấn luyện mô hình, tạo API Flask để nhận diện cảm xúc, và triển khai ứng dụng lên nền tảng cloud.

## Các bước triển khai

### Bước 1: Chuẩn bị dữ liệu
- Tải bộ dữ liệu FER2013 hoặc bộ dữ liệu khác hỗ trợ nhận diện cảm xúc (CK+, JAFFE).
- Xử lý ảnh: Resize ảnh, chuẩn hóa pixel (giá trị từ 0-255 thành 0-1).

### Bước 2: Xây dựng mô hình
- Xây dựng mô hình CNN với các lớp Convolutional, MaxPooling, và Fully Connected.
- Sử dụng các hàm kích hoạt như ReLU và Softmax.

### Bước 3: Huấn luyện mô hình
- Chia dữ liệu thành các tập train, validation và test.
- Huấn luyện mô hình với TensorFlow/Keras.

### Bước 4: Đánh giá mô hình
- Đánh giá mô hình bằng các metrics như accuracy, precision, recall và confusion matrix.

### Bước 5: Tạo API
- Sử dụng Flask để xây dựng API, cho phép người dùng tải ảnh và nhận dự đoán cảm xúc.
- Lưu mô hình đã huấn luyện và tải lại trong Flask API.

### Bước 6: Tạo giao diện web
- Tạo form HTML để người dùng tải ảnh lên.
- Kết nối API với giao diện người dùng thông qua Fetch API.

### Bước 7: Triển khai
- Sử dụng Docker để đóng gói ứng dụng và triển khai lên các nền tảng như Heroku, AWS, hoặc Google Cloud.

## Cấu trúc thư mục
emotion-detection-api/ ├── app.py # Flask API ├── model.py # Code mô hình CNN ├── requirements.txt # Danh sách các thư viện cần thiết ├── Dockerfile # Dockerfile cho triển khai ứng dụng ├── data/ # Dữ liệu huấn luyện (có thể tải về từ Kaggle) │ └── fer2013/ # Dữ liệu FER2013 ├── templates/ # Thư mục chứa các file HTML │ └── index.html # Giao diện web cho người dùng └── README.md # File README

## Cài đặt và Chạy Dự Án

### 1. Cài đặt yêu cầu
Tạo môi trường ảo và cài đặt các thư viện cần thiết bằng pip:

```bash
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate
pip install -r requirements.txt
