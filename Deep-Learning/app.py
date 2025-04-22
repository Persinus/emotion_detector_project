from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load mô hình emotion_detection_model.h5
model = load_model('emotion_detection_model.h5')

# Tạo một dictionary ánh xạ các nhãn của FER-2013
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Kiểm tra xem file có tồn tại không
        print(f"Received file: {file.filename}")

        # Mở và xử lý ảnh
        img = Image.open(file.stream)
        img = img.convert('L')
        img = img.resize((48, 48))

        # Chuyển ảnh thành mảng numpy và chuẩn bị đầu vào cho mô hình
        img_array = np.array(img)
        print(f"Image array shape: {img_array.shape}")  # In ra kích thước mảng ảnh

        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=-1)  # Thêm chiều kênh
        img_array = np.expand_dims(img_array, axis=0)  # Thêm chiều batch

        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_emotion = emotion_labels[predicted_class[0]]

        return jsonify({'prediction': predicted_emotion})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)