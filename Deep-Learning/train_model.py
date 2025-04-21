import numpy as np
import cv2
import tensorflow as tf

# Tải mô hình đã huấn luyện
model = tf.keras.models.load_model('emotion_detection_model_gsn.h5')

# Bản đồ các cảm xúc
emotion_dict = {
    0: "Angry",
    1: "Disgusted",
    2: "Fearful",
    3: "Happy",
    4: "Neutral",
    5: "Sad",
    6: "Surprised"
}

# Đường dẫn đến ảnh cần dự đoán
image_path = 'path/to/image.jpg'  # Thay thế bằng đường dẫn đến ảnh của bạn

# Đọc ảnh
image = cv2.imread(image_path)

if image is None:
    print(f"Không thể đọc ảnh từ: {image_path}")
else:
    # Chuyển ảnh sang thang xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Phát hiện khuôn mặt sử dụng Haar Cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        print("Không phát hiện được khuôn mặt trong ảnh.")
    else:
        for (x, y, w, h) in faces:
            # Vẽ khung xung quanh khuôn mặt
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Trích xuất và resize khuôn mặt về 48x48
            roi_gray = gray[y:y + h, x:x + w]
            resized_face = cv2.resize(roi_gray, (48, 48))
            cropped_img = np.expand_dims(np.expand_dims(resized_face, -1), 0)

            # Dự đoán cảm xúc
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            emotion = emotion_dict[maxindex]

            # Ghi tên cảm xúc lên ảnh
            cv2.putText(
                image,
                emotion,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

        # Hiển thị ảnh với cảm xúc
        cv2.imshow("Emotion Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()