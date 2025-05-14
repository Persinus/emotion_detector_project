<template>
  <div class="app-container">
    <h1>Emotion Detection</h1>

    <!-- Two-column layout -->
    <div class="content-container">
      <!-- Left Column: Upload Image -->
      <div class="left-panel">
        <h3>Upload Image</h3>
        <div class="image-preview">
          <img :src="imagePreview" alt="Original Image" v-if="imagePreview" />
          <p v-if="!selectedImage" class="no-image">
            No image selected yet. Please upload a close-up image of a face.
          </p>
        </div>
        <input type="file" @change="onFileChange" class="file-input" />
        <button
          @click="makePrediction"
          :disabled="!faceDetected || isLoading"
          class="predict-button"
        >
          {{ isLoading ? "Processing..." : "Predict Emotion" }}
        </button>
        <div v-if="isDetecting" class="loading-indicator">
          <p>Detecting face...</p>
        </div>
      </div>

      <!-- Right Column: Results -->
      <div class="right-panel">
        <h3>Results</h3>
        <div class="image-preview">
          <canvas ref="resultCanvas" v-if="faceDetected"></canvas>
        </div>
        <div class="results">
          <p v-if="prediction" class="prediction-result">
            Trạng thái cảm xúc của ảnh là : {{ prediction }}
          </p>
          <p v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as faceapi from "face-api.js";
import axios from "axios"; // Import axios

export default {
  data() {
    return {
      selectedImage: null, // Selected file
      imagePreview: null, // URL for preview
      faceDetected: false, // Face detection status
      errorMessage: null, // Error message to display
      isLoading: false, // Loading state for prediction
      isDetecting: false, // Loading state for face detection
      prediction: null, // Prediction result
      croppedFaceBlob: null, // Cropped face image blob
    };
  },
  methods: {
    async onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedImage = file;
        this.imagePreview = URL.createObjectURL(file);
        this.errorMessage = null;
        this.faceDetected = false;

        console.log("Image selected:", file.name);

        // Run face detection
        this.isDetecting = true;
        await this.detectFace(file);
        this.isDetecting = false;
      }
    },
    async detectFace(file) {
      try {
        console.log("Loading face detection model...");
        await faceapi.nets.ssdMobilenetv1.loadFromUri("/models");

        console.log("Model loaded. Detecting face...");
        const image = await faceapi.bufferToImage(file);
        const detections = await faceapi.detectSingleFace(image);

        if (detections) {
          console.log("Face detected:", detections);
          this.faceDetected = true;

          // Wait for DOM updates before accessing canvas
          await this.$nextTick();

          // Access canvas
          const canvas = this.$refs.resultCanvas;
          if (!canvas) {
            throw new Error("Canvas element not found.");
          }

          const context = canvas.getContext("2d");
          const { x, y, width, height } = detections.box;

          const img = new Image();
          img.src = this.imagePreview;

          // Draw the image and the face bounding box
          await new Promise((resolve) => {
            img.onload = () => {
              canvas.width = img.width;
              canvas.height = img.height;
              context.drawImage(img, 0, 0, img.width, img.height);

              // Draw rectangle around detected face
              context.strokeStyle = "red";
              context.lineWidth = 2;
              context.strokeRect(x, y, width, height);

              // Crop the detected face and save it as a blob
              const faceCanvas = document.createElement("canvas");
              faceCanvas.width = width;
              faceCanvas.height = height;
              const faceContext = faceCanvas.getContext("2d");
              faceContext.drawImage(img, x, y, width, height, 0, 0, width, height);
              faceCanvas.toBlob((blob) => {
                this.croppedFaceBlob = blob;
                console.log("Cropped face blob created.");
              });

              resolve();
            };
          });
        } else {
          console.warn("No face detected in the image.");
          this.errorMessage =
            "No face detected in the image. Please upload a closer image.";
          this.faceDetected = false;
        }
      } catch (error) {
        console.error("Error detecting face:", error);
        this.errorMessage = "Error detecting face: " + error.message;
        this.faceDetected = false;
      }
    },
    async makePrediction() {
      if (!this.faceDetected || !this.croppedFaceBlob) {
        this.errorMessage = "Please upload an image with a detectable face to analyze!";
        return;
      }

      try {
        this.isLoading = true;
        this.errorMessage = null;

        console.log("Sending cropped face to backend for prediction...");

        const formData = new FormData();
        formData.append("file", this.croppedFaceBlob, "cropped_face.jpg");

        const response = await axios.post("http://127.0.0.1:5000//predict_image", formData, {
        
        });

        if (response.data && response.data.prediction) {
          console.log("Prediction received:", response.data);
          this.prediction = response.data.prediction;
        } else {
          throw new Error("Prediction data is invalid.");
        }
      } catch (error) {
        console.error("Error connecting to backend:", error);
        this.errorMessage = "Cannot connect to backend. Please make sure it is running.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Overall app styling */
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;
 
  font-family: 'Segoe UI', Arial, sans-serif;
  background: linear-gradient(120deg, #e0f7fa 60%, #f9f9f9 100%);
}

h1 {
  color: #007bff;
  margin-bottom: 24px;
  font-size: 2.2rem;
  letter-spacing: 1px;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,123,255,0.08);
}

/* Two-column layout */
.content-container {
  display: flex;
  gap: 32px;
  width: 100%;
  min-width: 1200px;
  height: 80vh; /* Chiếm 80% chiều cao màn hình */
  min-height: 400px;
  align-items: stretch;
  background: rgba(255,255,255,0.7);
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0,123,255,0.08);
  padding: 32px 24px;
  transition: box-shadow 0.3s;
}

.left-panel,
.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  padding: 24px 18px;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0, 123, 255, 0.06);
  height: 100%;
  justify-content: flex-start;
  transition: box-shadow 0.3s, transform 0.2s;
}

.left-panel:hover,
.right-panel:hover {
  box-shadow: 0 6px 24px rgba(0,123,255,0.13);
  transform: translateY(-2px) scale(1.01);
}

h3 {
  color: #0097a7;
  margin-bottom: 12px;
  font-weight: 600;
  font-size: 1.2rem;
}

.image-preview {
  margin-bottom: 18px;
  width: 100%;
  text-align: center;
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 320px; /* Đặt chiều cao tối thiểu cho vùng ảnh/canvas */
  max-height: 48vh;
}

.image-preview img,
canvas {
  max-width: 100%;
  max-height: 300px; /* Đặt chiều cao tối đa cho ảnh/canvas */
  min-height: 220px; /* Đặt chiều cao tối thiểu cho ảnh/canvas */
  border-radius: 10px;
  border: 2px solid #b2ebf2;
  object-fit: contain;
  box-shadow: 0 2px 12px rgba(0,123,255,0.07);
  background: #f5fafd;
  animation: fadeIn 0.7s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.no-image {
  color: #ff6b6b;
  font-size: 16px;
  font-style: italic;
  margin-top: 20px;
}

.file-input {
  margin-bottom: 14px;
  padding: 7px 10px;
  border-radius: 6px;
  border: 1.5px solid #b2ebf2;
  background: #fafdff;
  transition: border 0.3s;
}
.file-input:focus {
  border: 2px solid #007bff;
}

.predict-button {
  padding: 12px 28px;
  background: linear-gradient(90deg, #007bff 60%, #00bcd4 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 10px;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(0,123,255,0.08);
}

.predict-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.predict-button:hover:not(:disabled) {
  background: linear-gradient(90deg, #0056b3 60%, #0097a7 100%);
  transform: translateY(-2px) scale(1.04);
  box-shadow: 0 4px 16px rgba(0,123,255,0.13);
}

.loading-indicator {
  margin-top: 10px;
  color: #007bff;
  font-size: 15px;
  font-style: italic;
  animation: pulse 1.2s infinite;
}
@keyframes pulse {
  0% { opacity: 0.7; }
  50% { opacity: 1; }
  100% { opacity: 0.7; }
}

.results {
  width: 100%;
  margin-top: 10px;
  text-align: center;
}

.prediction-result {
  font-size: 1.2rem;
  color: #007bff;
  font-weight: bold;
  margin-top: 1rem;
  animation: fadeIn 1s;
}

.error-message {
  color: #e53935;
  font-weight: bold;
  margin-top: 1rem;
  animation: shake 0.4s;
}
@keyframes shake {
  10%, 90% { transform: translateX(-2px);}
  20%, 80% { transform: translateX(4px);}
  30%, 50%, 70% { transform: translateX(-8px);}
  40%, 60% { transform: translateX(8px);}
}

/* Responsive cho mobile */
@media (max-width: 1100px) {
  .content-container {
    max-width: 98vw;
    padding: 18px 2vw;
    gap: 12px;
  }
}
@media (max-width: 900px) {
  .content-container {
    flex-direction: column;
    height: auto;
    min-height: unset;
    padding: 12px 2vw;
  }
  .left-panel,
  .right-panel {
    height: auto;
    margin-bottom: 10px;
  }
  .image-preview img,
  canvas {
    max-height: 32vh;
  }
}
</style>
