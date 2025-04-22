<template>
  <div class="webcam-container">
    <h1 class="title">Webcam Emotion Detection</h1>
    <div class="row">
      <!-- Phần webcam (6/10 chiều rộng) -->
      <div class="col-6 video-container">
        <video ref="video" autoplay muted></video>
        <canvas ref="overlay"></canvas>
      </div>

      <!-- Phần nút và chú thích (4/10 chiều rộng) -->
      <div class="col-4 controls-container">
        <div class="button-container">
          <button @click="startWebcam" class="start-button">Mở Webcam</button>
          <button @click="stopWebcam" class="stop-button">Tắt Webcam</button>
        </div>
        <div class="info-container">
          <h3 class="info-title">Hướng dẫn:</h3>
          <p class="info-text">Đặt khuôn mặt bạn vào giữa khung hình để hệ thống nhận diện cảm xúc.</p>
          <h3 class="info-title">Kết quả nhận diện:</h3>
          <p class="emotion-result">Cảm xúc: {{ emotion }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as faceapi from 'face-api.js';

export default {
  data() {
    return {
      stream: null,
      emotion: "Chưa xác định",
    };
  },
  methods: {
    async loadModels() {
      const MODEL_URL = "";
      await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
      await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
      await faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);
      console.log("Models loaded successfully.");
    },

    async startWebcam() {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          await this.loadModels();
          this.stream = await navigator.mediaDevices.getUserMedia({ video: {} });
          this.$refs.video.srcObject = this.stream;
          this.detectEmotions();
        } catch (error) {
          console.error("Lỗi khi mở webcam: ", error);
        }
      } else {
        alert("Trình duyệt không hỗ trợ webcam.");
      }
    },

    stopWebcam() {
      if (this.stream) {
        let tracks = this.stream.getTracks();
        tracks.forEach((track) => track.stop());
        this.stream = null;
      }
    },

    async detectEmotions() {
      const video = this.$refs.video;
      const canvas = this.$refs.overlay;
      const displaySize = { width: video.videoWidth, height: video.videoHeight };

      faceapi.matchDimensions(canvas, displaySize);

      setInterval(async () => {
        const detections = await faceapi
          .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
          .withFaceLandmarks()
          .withFaceExpressions();

        const resizedDetections = faceapi.resizeResults(detections, displaySize);
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);

        faceapi.draw.drawDetections(canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

        if (detections.length > 0) {
          const expressions = detections[0].expressions;
          const sorted = Object.entries(expressions).sort((a, b) => b[1] - a[1]);
          this.emotion = sorted[0][0];
        } else {
          this.emotion = "Không phát hiện khuôn mặt";
        }
      }, 100);
    },
  },
};
</script>

<style scoped>
/* Tổng thể */
.webcam-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  min-height: 100vh;
  padding: 40px;
  text-align: center;
  border-radius: 12px;
}

/* Tiêu đề */
.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #0d47a1;
  margin-bottom: 30px;
}

/* Layout chia cột */
.row {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

/* Video container */
.video-container {
  flex: 6;
  position: relative;
  border: 4px solid #90caf9;
  border-radius: 12px;
  background-color: #000;
  height: 480px;
  display: flex;
  align-items: center;
  justify-content: center;
}

video {
  width: 100%;
  height: 100%;
  border-radius: 12px;
  object-fit: cover;
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* Controls container */
.controls-container {
  flex: 4;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 20px;
}

/* Button container */
.button-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

/* Nút bấm */
button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1.2rem;
  font-weight: bold;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.start-button {
  background-color: #4caf50;
  color: white;
}

.start-button:hover {
  background-color: #45a049;
  transform: scale(1.05);
}

.stop-button {
  background-color: #f44336;
  color: white;
}

.stop-button:hover {
  background-color: #e53935;
  transform: scale(1.05);
}

/* Info container */
.info-container {
  margin-top: 20px;
}

.info-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #0d47a1;
  margin-bottom: 10px;
}

.info-text {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 20px;
}

.emotion-result {
  font-size: 1.2rem;
  color: #0d47a1;
  font-weight: bold;
}
</style>
