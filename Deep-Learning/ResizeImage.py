import os
import cv2

# Đường dẫn tới file ảnh
file_path = "test1.png"  # Thay bằng đường dẫn đầy đủ nếu cần

# Kiểm tra sự tồn tại của file
if os.path.exists(file_path):
    print("File tồn tại:", file_path)

    # Đọc ảnh từ file
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    if image is not None:
        # Resize ảnh về kích thước 48x48
        resized_image = cv2.resize(image, (48, 48))

        # Hiển thị ảnh sau khi resize
        cv2.imshow("Resized Image", resized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print("Resize thành công!")
    else:
        print("File không thể đọc được dưới dạng ảnh. Định dạng có thể không hợp lệ.")
else:
    print("File không tồn tại:", file_path)