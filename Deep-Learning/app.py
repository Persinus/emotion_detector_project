from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from flask_cors import CORS
import io
import base64

app = Flask(__name__)

# Cấu hình CORS cho phép yêu cầu từ localhost và từ domain đã deploy
CORS(app, resources={r"/predict": {"origins": ["http://localhost:5173", "https://emotion-detector-project-chaos.onrender.com"]}})
CORS(app, resources={r"/predict_frame": {"origins": ["http://localhost:5173", "https://emotion-detector-project-chaos.onrender.com"]}})
CORS(app, resources={r"/status": {"origins": ["http://localhost:5173", "https://emotion-detector-project-chaos.onrender.com"]}})

# Load the emotion detection model
model = load_model('emotion_detection_model.h5')

# Emotion labels from FER-2013 dataset
emotion_labels = ['Angry 😡', 'Disgust 🤢', 'Fear 😨', 'Happy 😄', 'Sad 😢', 'Surprise 😲', 'Neutral 😐']

@app.route('/predict', methods=['POST'])
def predict():
    """Predict emotion from a static image file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        print(f"Received file: {file.filename}")
        
        # Open and process the image
        img = Image.open(file.stream)
        img = img.convert('L')  # Convert image to grayscale
        img = img.resize((48, 48))  # Resize to match model input

        # Prepare the image for prediction
        img_array = np.array(img)
        print(f"Image array shape: {img_array.shape}")  # Debugging log

        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Predict the emotion
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_emotion = emotion_labels[predicted_class[0]]

        return jsonify({'prediction': predicted_emotion})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_frame', methods=['POST'])
def predict_frame():
    """Predict emotion from a video frame (real-time prediction)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        print(f"Received frame: {file.filename}")
        
        # Open and process the image frame
        img = Image.open(file.stream)
        img = img.convert('L')  # Convert to grayscale
        img = img.resize((48, 48))  # Resize to match model input

        # Prepare the frame for prediction
        img_array = np.array(img)
        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=-1)  # Add channel dimension
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

        # Predict emotion from the frame
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)
        predicted_emotion = emotion_labels[predicted_class[0]]

        return jsonify({'prediction': predicted_emotion})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/status', methods=['GET'])
def status():
    """Health check to verify if the service is running"""
    try:
        return jsonify({'status': 'success', 'message': 'Emotion detection service is running!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
