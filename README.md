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

Bước 6: Tạo giao diện web
Sử dụng Vue 3 để phát triển giao diện người dùng (frontend).

Sử dụng Face API để phát hiện và cắt khuôn mặt từ ảnh trước khi gửi dữ liệu đến API Flask.

Kết nối API Flask với giao diện người dùng bằng Axios để gửi và nhận dữ liệu.

Các bước cụ thể:
Cài đặt Face API:

Cài đặt thư viện face-api.js thông qua npm:

npm install face-api.js
Xử lý ảnh trên frontend:

Dùng Face API để phát hiện khuôn mặt và cắt khuôn mặt từ ảnh.

Gửi khuôn mặt đã được xử lý qua Axios đến API Flask.

Xây dựng giao diện với Vue 3:

Tạo một form cho phép người dùng tải ảnh lên.

Hiển thị kết quả dự đoán cảm xúc sau khi API trả về.

Kết nối với Flask API:

Sử dụng Axios để gửi request đến API Flask:


## Cài đặt và Chạy Dự Án

### 1. Cài đặt yêu cầu
Tạo môi trường ảo và cài đặt các thư viện cần thiết bằng pip:


