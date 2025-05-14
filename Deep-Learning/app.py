from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import librosa
import tensorflow as tf
import os
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Kích hoạt CORS cho toàn bộ ứng dụng

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load emotion detection model for images
model_image = load_model('emotion_detection_model.h5')

# Load emotion detection model for audio
MODEL_PATH = "emotion_audio_model.keras"
model_audio = tf.keras.models.load_model(MODEL_PATH)

# Emotion labels for image model (from FER-2013 dataset)
emotion_labels_image = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Emotion labels for audio model
emotion_labels_audio = ['Angry', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Các tham số xử lý âm thanh
AUDIO_SAMPLE_RATE = 22050
AUDIO_DURATION = 3
MFCC_FEATURES = 40

def preprocess_audio(file_path):
    """Hàm xử lý âm thanh, trích xuất đặc trưng MFCC."""
    audio, sr = librosa.load(file_path, sr=AUDIO_SAMPLE_RATE, duration=AUDIO_DURATION)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=MFCC_FEATURES)

    target_width = int(AUDIO_SAMPLE_RATE * AUDIO_DURATION // 512)
    if mfcc.shape[1] < target_width:
        padded = np.zeros((MFCC_FEATURES, target_width))
        padded[:, :mfcc.shape[1]] = mfcc
    else:
        padded = mfcc[:, :target_width]
    return padded[..., np.newaxis]  # Thêm chiều kênh

@app.route('/predict_image', methods=['POST'])
def predict_image():
    """Dự đoán cảm xúc từ tệp hình ảnh tải lên."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        print(f"Received file: {file.filename}")
        
        # Open and process the image
        img = Image.open(file.stream).convert('L')  # Chuyển sang ảnh xám
        img = img.resize((48, 48))  # Resize để phù hợp với đầu vào mô hình

        # Prepare the image for prediction
        img_array = np.array(img).astype('float32') / 255.0  # Chuẩn hóa
        img_array = np.expand_dims(img_array, axis=-1)  # Thêm chiều kênh (48, 48, 1)
        img_array = np.expand_dims(img_array, axis=0)   # Thêm chiều batch (1, 48, 48, 1)

        print(f"Image array shape: {img_array.shape}")  # Kiểm tra kích thước đầu vào

        # Predict the emotion
        predictions = model_image.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_emotion = emotion_labels_image[predicted_class[0]]

        return jsonify({'prediction': predicted_emotion})

    except Exception as e:
        print("Error occurred:", e)  # In ra lỗi chi tiết
        return jsonify({'error': str(e)}), 500

@app.route('/predict_audio', methods=['POST'])
def predict_audio():
    """Dự đoán cảm xúc từ tệp âm thanh tải lên."""
    if 'file' not in request.files:
        logging.error("Không tìm thấy tệp trong yêu cầu.")
        return jsonify({"error": "No file uploaded."}), 400

    file = request.files['file']
    if file.filename == '':
        logging.error("Tên tệp trống.")
        return jsonify({"error": "No file selected."}), 400

    # Kiểm tra loại tệp
    if not file.filename.lower().endswith(('.mp3', '.wav')):
        logging.error("Tệp không phải là MP3 hoặc WAV.")
        return jsonify({"error": "Invalid file format. Please upload MP3 or WAV files."}), 400

    # Lưu tạm tệp âm thanh
    temp_path = os.path.join("temp", file.filename)
    try:
        file.save(temp_path)
        logging.info(f"Tệp đã được lưu tạm tại: {temp_path}")

        # Tiền xử lý âm thanh
        processed_audio = preprocess_audio(temp_path)
        processed_audio = np.expand_dims(processed_audio, axis=0)  # Thêm batch size

        # Dự đoán cảm xúc
        predictions = model_audio.predict(processed_audio)
        predicted_label = emotion_labels_audio[np.argmax(predictions)]
        logging.info(f"Dự đoán: {predicted_label}")

        # Xóa tệp tạm
        os.remove(temp_path)
        return jsonify({"emotion": predicted_label})
    except Exception as e:
        # Log lỗi chi tiết
        logging.error(f"Lỗi xảy ra: {e}", exc_info=True)
        os.remove(temp_path)
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Kiểm tra trạng thái của dịch vụ"""
    return jsonify({'status': 'success', 'message': 'Emotion detection service is running!'}), 200

if __name__ == '__main__':
    # Đảm bảo thư mục temp tồn tại
    os.makedirs("temp", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
