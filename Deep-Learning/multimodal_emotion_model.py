import tensorflow as tf
import numpy as np
import librosa
import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# ------------------ CONSTANTS ------------------
IMG_WIDTH, IMG_HEIGHT = 48, 48
AUDIO_SAMPLE_RATE = 22050
AUDIO_DURATION = 3
MFCC_FEATURES = 40
BATCH_SIZE = 32
EPOCHS = 25
NUM_CLASSES = 7

# ------------------ IMAGE DATA PREPROCESSING ------------------
image_datagen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_image_generator = image_datagen.flow_from_directory(
    './Dataset/Train-FER-2013',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    class_mode='categorical'
)

validation_image_generator = image_datagen.flow_from_directory(
    './Dataset/Test-FER-2013',
    target_size=(IMG_WIDTH, IMG_HEIGHT),
    batch_size=BATCH_SIZE,
    color_mode='grayscale',
    class_mode='categorical'
)

# ------------------ AUDIO DATA PREPROCESSING ------------------
def preprocess_audio(file_path):
    audio, sr = librosa.load(file_path, sr=AUDIO_SAMPLE_RATE, duration=AUDIO_DURATION)
    mfcc = librosa.feature.mfcc(audio, sr=sr, n_mfcc=MFCC_FEATURES)
    padded_mfcc = np.zeros((MFCC_FEATURES, int(AUDIO_SAMPLE_RATE * AUDIO_DURATION // 512)))
    padded_mfcc[:, :mfcc.shape[1]] = mfcc
    return padded_mfcc[..., np.newaxis]

def audio_data_generator(directory, batch_size):
    while True:
        files = os.listdir(directory)
        np.random.shuffle(files)
        for i in range(0, len(files), batch_size):
            batch_files = files[i:i + batch_size]
            batch_data = [preprocess_audio(os.path.join(directory, file)) for file in batch_files]
            batch_labels = [int(file.split('_')[0]) for file in batch_files]
            yield np.array(batch_data), tf.keras.utils.to_categorical(batch_labels, NUM_CLASSES)

train_audio_generator = audio_data_generator('./Dataset/Train-RAVDESS', BATCH_SIZE)
validation_audio_generator = audio_data_generator('./Dataset/Test-RAVDESS', BATCH_SIZE)
# ------------------ IMAGE MODEL ------------------
image_input = Input(shape=(IMG_WIDTH, IMG_HEIGHT, 1))
x = Conv2D(32, (3, 3), activation='relu')(image_input)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Dropout(0.25)(x)
x = Conv2D(64, (3, 3), activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Dropout(0.25)(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
image_branch = Dense(64, activation='relu')(x)

# ------------------ AUDIO MODEL ------------------
audio_input = Input(shape=(MFCC_FEATURES, int(AUDIO_SAMPLE_RATE * AUDIO_DURATION // 512), 1))
y = Conv2D(32, (3, 3), activation='relu')(audio_input)
y = MaxPooling2D(pool_size=(2, 2))(y)
y = Dropout(0.25)(y)
y = Conv2D(64, (3, 3), activation='relu')(y)
y = MaxPooling2D(pool_size=(2, 2))(y)
y = Dropout(0.25)(y)
y = Flatten()(y)
y = Dense(128, activation='relu')(y)
y = Dropout(0.5)(y)
audio_branch = Dense(64, activation='relu')(y)

# ------------------ COMBINED MODEL ------------------
combined = concatenate([image_branch, audio_branch])
z = Dense(128, activation='relu')(combined)
z = Dropout(0.5)(z)
output = Dense(NUM_CLASSES, activation='softmax')(z)

model = Model(inputs=[image_input, audio_input], outputs=output)
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Kết hợp các generators
train_steps = min(len(train_image_generator), len(os.listdir('./Dataset/Train-RAVDESS')) // BATCH_SIZE)
validation_steps = min(len(validation_image_generator), len(os.listdir('./Dataset/Test-RAVDESS')) // BATCH_SIZE)

history = model.fit(
    zip(train_image_generator, train_audio_generator),
    steps_per_epoch=train_steps,
    validation_data=zip(validation_image_generator, validation_audio_generator),
    validation_steps=validation_steps,
    epochs=EPOCHS
)

model.save('multimodal_emotion_model.h5')

# Dự đoán xác suất cho ảnh và âm thanh
img_preds = model.predict([val_img_data, val_audio_data])

# Voting: chọn nhãn có xác suất cao nhất từ ảnh hoặc âm thanh
voted_preds = []
for i in range(len(img_preds)):
    img_pred = np.argmax(img_preds[i][:NUM_CLASSES])
    audio_pred = np.argmax(img_preds[i][NUM_CLASSES:])
    
    if img_pred == audio_pred:
        voted_preds.append(img_pred)
    else:
        if img_preds[i][img_pred] > img_preds[i][audio_pred]:
            voted_preds.append(img_pred)
        else:
            voted_preds.append(audio_pred)

y_true = np.argmax(val_img_labels, axis=1)

# Hiển thị confusion matrix
cm = confusion_matrix(y_true, voted_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=validation_image_generator.class_indices)
disp.plot(cmap=plt.cm.Greens)
plt.title("Confusion Matrix with Voting (Image + Audio)")
plt.show()

# Biểu đồ xác suất của một mẫu bất kỳ
sample_idx = 0

plt.figure(figsize=(10, 4))
plt.bar(range(NUM_CLASSES), img_preds[sample_idx][:NUM_CLASSES], alpha=0.5, label='Image')
plt.bar(range(NUM_CLASSES), img_preds[sample_idx][NUM_CLASSES:], alpha=0.5, label='Audio')
plt.bar(range(NUM_CLASSES), (img_preds[sample_idx][:NUM_CLASSES] + img_preds[sample_idx][NUM_CLASSES:]) / 2, alpha=0.8, label='Voted', linestyle='dashed')
plt.xticks(range(NUM_CLASSES), list(validation_image_generator.class_indices.keys()))
plt.ylabel("Probability")
plt.title(f"Prediction Probabilities for Sample #{sample_idx}")
plt.legend()
plt.show()

# Đồ thị Loss trong quá trình huấn luyện
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss during Training and Validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Đồ thị Accuracy trong quá trình huấn luyện
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Accuracy during Training and Validation')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()
 