from tensorflow.keras.models import load_model

# Load mô hình đã huấn luyện xong (.h5)
model = load_model('emotion_detection_model.h5')

# Lưu lại mô hình theo định dạng mới
model.save('emotion_model_tf', save_format='tf')
