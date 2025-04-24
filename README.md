# Emotion Detector Project

## Overview
This project uses a deep learning model (CNN) to detect emotions from images. The model is trained on datasets like FER2013 and integrates with a Flask API for emotion detection. Additionally, a Vue 3 web interface is developed for user interaction.

---

## Features
- **Emotion Detection:** Detects emotions such as Angry, Happy, Sad, etc., from facial images.
- **Real-time Webcam Support:** Enables real-time emotion detection using a webcam.
- **Web Interface:** Provides an intuitive frontend built with Vue 3.
- **API Integration:** Backend powered by Flask, connecting the model and the web interface.

---

## Implementation Steps

### Step 1: Data Preparation
- **Datasets:** Use datasets like FER2013, CK+, or JAFFE for training.
- **Preprocessing:**
  - Resize images to 48x48 pixels (grayscale).
  - Normalize pixel values to range [0, 1].

---

### Step 2: Build the Model
- **Architecture:** Build a Convolutional Neural Network (CNN) with:
  - Convolutional layers
  - MaxPooling layers
  - Fully connected layers
- **Activation Functions:** Use ReLU for hidden layers and Softmax for the output layer.

---

### Step 3: Train the Model
- **Data Splits:** Divide the dataset into training, validation, and test sets.
- **Training Framework:** Use TensorFlow/Keras.
- **Evaluation Metrics:** Track metrics like accuracy, precision, recall, and confusion matrix.

---

### Step 4: Deploy API
- **Framework:** Use Flask to build a RESTful API.
- **Functionality:**
  - Accept uploaded images.
  - Process images and return emotion predictions.
- **Model Integration:** Load the trained model within the Flask app.

---

### Step 5: Web Interface Development
#### Tools:
- **Frontend Framework:** Vue 3.
- **Face Detection Library:** `face-api.js` for detecting and cropping faces.

#### Steps:
1. **Install Face API:**
   ```bash
   npm install face-api.js
