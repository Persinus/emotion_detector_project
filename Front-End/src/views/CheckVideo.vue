<template>
  <div class="container">
    <div class="main">
      <!-- Video -->
      <video ref="videoRef" autoplay muted></video>
      <!-- Canvas -->
      <canvas ref="canvasRef"></canvas>
    </div>

    <!-- Loading message -->
    <p v-if="loading" class="loading">Loading models...</p>

    <!-- Kết quả quét -->
    <div class="results" v-if="!loading && emotion">
      <h3>Kết quả quét:</h3>
      <p class="emotion-result">Cảm xúc: {{ emotion }}</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import * as faceapi from "face-api.js";

export default {
  setup() {
    const videoRef = ref(null);
    const canvasRef = ref(null);
    const isLoaded = ref(false);
    const loading = ref(true);
    const emotion = ref("");

    // Hàm load models của face-api.js
    const loadModels = async () => {
      await faceapi.nets.ssdMobilenetv1.loadFromUri("/models");
      await faceapi.nets.faceLandmark68Net.loadFromUri("/models");
      await faceapi.nets.faceExpressionNet.loadFromUri("/models");
    };

    // Hàm lấy video stream
    const getVideoStream = async () => {
      return await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });
    };

    // Gửi frame video đến Flask server
    const sendFrameToServer = async (frame) => {
      try {
        const formData = new FormData();
        formData.append("file", frame);

        const response = await fetch("http://127.0.0.1:5000/predict_frame", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        if (data.prediction) {
          emotion.value = data.prediction;
        }
      } catch (error) {
        console.error("Error sending frame to server:", error);
      }
    };

    onMounted(async () => {
      const displaySize = {
        width: 0,
        height: 0,
      };

      const start = async () => {
        if (!videoRef.value || !canvasRef.value) return;

        // Lấy stream video
        const stream = await getVideoStream();
        videoRef.value.srcObject = stream;

        // Load các model cần thiết
        await loadModels();

        videoRef.value.pause();
        videoRef.value.play();

        videoRef.value.addEventListener("playing", () => {
          if (!videoRef.value || !canvasRef.value) return;

          // Đồng bộ kích thước video và canvas
          displaySize.width = videoRef.value.videoWidth;
          displaySize.height = videoRef.value.videoHeight;

          canvasRef.value.width = displaySize.width;
          canvasRef.value.height = displaySize.height;

          faceapi.matchDimensions(canvasRef.value, displaySize);
        });

        isLoaded.value = true;
        loading.value = false;
      };

      const loop = async () => {
        if (!videoRef.value || !canvasRef.value || !isLoaded.value) {
          return;
        }

        if (displaySize.width === 0 || displaySize.height === 0) return;

        // Phát hiện khuôn mặt
        const detections = await faceapi
          .detectAllFaces(videoRef.value, new faceapi.SsdMobilenetv1Options())
          .withFaceLandmarks()
          .withFaceExpressions();

        // Điều chỉnh kết quả phát hiện theo kích thước video
        const resizedDetections = faceapi.resizeResults(detections, displaySize);

        // Làm sạch canvas trước khi vẽ
        const context = canvasRef.value.getContext("2d");
        context.clearRect(0, 0, displaySize.width, displaySize.height);

        // Vẽ kết quả phát hiện lên canvas
        faceapi.draw.drawDetections(canvasRef.value, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvasRef.value, resizedDetections);

        // Cập nhật cảm xúc nếu phát hiện khuôn mặt
        if (detections.length > 0) {
          const expressions = detections[0].expressions;
          const sorted = Object.entries(expressions).sort((a, b) => b[1] - a[1]);
          emotion.value = sorted[0][0]; // Cảm xúc có xác suất cao nhất
        }
      };

      start();

      const interval = setInterval(loop, 100);

      // Cleanup interval khi component bị hủy
      onUnmounted(() => {
        clearInterval(interval);
      });
    });

    return {
      videoRef,
      canvasRef,
      loading,
      emotion,
    };
  },
};
</script>

<style scoped>
.container {
  position: relative;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.main {
  position: relative;
  width: 100%;
  height: auto;
}

video {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 10px;
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  border-radius: 10px;
}

.loading {
  font-size: 18px;
  color: #fff;
  text-align: center;
  margin-top: 10px;
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  border-radius: 5px;
}

.results {
  margin-top: 20px;
  text-align: center;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 20px;
  border-radius: 10px;
}

.results h3 {
  font-size: 24px;
  margin-bottom: 10px;
  font-weight: bold;
  text-transform: uppercase;
}

.emotion-result {
  font-size: 22px;
  font-weight: 600;
  color: #ffeb3b;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
}
</style>
