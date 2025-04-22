from PIL import Image

# Đường dẫn tới ảnh gốc
input_path = "./test1.png"  # Thay bằng đường dẫn tới ảnh gốc của bạn
output_path = "output_image.png"  # Đường dẫn lưu ảnh sau khi xử lý

# Mở ảnh gốc
img = Image.open(input_path)

# Chuyển ảnh sang grayscale
img_gray = img.convert("L")

# Thay đổi kích thước ảnh thành 48x48
img_resized = img_gray.resize((48, 48))

# Lưu ảnh kết quả
img_resized.save(output_path)

print(f"Ảnh đã được chuyển đổi và lưu tại: {output_path}")