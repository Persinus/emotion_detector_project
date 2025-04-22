import cv2
import tensorflow as tf
import numpy as np

# Load the pre-trained model
model = tf.keras.models.load_model('emotion_detection_model.h5')

# Define emotion labels (adjust to match your model's output classes)
labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Start webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Define the frame size for model input
frame_size = (48, 48)  # Adjusted to match model's input shape (48x48, grayscale)

# Load pre-trained Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # If faces are detected, process the first one
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Extract the face from the frame
        face = gray_frame[y:y + h, x:x + w]
        resized_face = cv2.resize(face, frame_size)  # Resize to 48x48
        normalized_face = resized_face / 255.0  # Normalize pixel values
        input_face = np.expand_dims(normalized_face, axis=-1)  # Add channel dimension
        input_face = np.expand_dims(input_face, axis=0)  # Add batch dimension

        # Predict emotion
        predictions = model.predict(input_face)
        label_index = np.argmax(predictions)
        label = labels[label_index]

        # Display prediction on frame
        cv2.putText(frame, f'Prediction: {label}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the webcam feed with face and prediction
    cv2.imshow('Webcam', frame)

    # Break loop on 'q' key press (or 'X' key in the window)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()