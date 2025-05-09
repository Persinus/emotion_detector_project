<template>
  <div class="container">
    <!-- Loading Modal -->
    <div v-if="loading" class="modal">
      <div class="modal-content">🧠 Xin chờ... đang tải mô hình...</div>
    </div>

    <!-- Ready Dialog -->
    <div v-if="readyDialog" class="modal ready">
      <div class="modal-content success">✅ Mô hình đã sẵn sàng! Bắt đầu quét</div>
    </div>

    <!-- Main Split Layout -->
    <div class="main">
      <div class="left-panel">
        <video ref="videoRef" autoplay muted playsinline></video>
        <canvas ref="canvasRef"></canvas>
      </div>
      <div class="right-panel">
        <div v-if="emotion">
          <h3>Kết quả quét</h3>
          <p class="emotion-result">Cảm xúc: {{ emotion }}</p>
        </div>
      </div>
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
    const loading = ref(true);
    const emotion = ref("");
    const isLoaded = ref(false);
    const readyDialog = ref(false);

    const loadModels = async () => {
      await faceapi.nets.ssdMobilenetv1.loadFromUri("/models");
      await faceapi.nets.faceLandmark68Net.loadFromUri("/models");
      await faceapi.nets.faceExpressionNet.loadFromUri("/models");
    };

    const getVideoStream = async () => {
      return await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });
    };

    onMounted(async () => {
      const displaySize = {
        width: 0,
        height: 0,
      };

      const start = async () => {
        const stream = await getVideoStream();
        videoRef.value.srcObject = stream;

        await loadModels();
        videoRef.value.pause();
        videoRef.value.play();

        videoRef.value.addEventListener("playing", () => {
          displaySize.width = videoRef.value.videoWidth;
          displaySize.height = videoRef.value.videoHeight;

          canvasRef.value.width = displaySize.width;
          canvasRef.value.height = displaySize.height;

          faceapi.matchDimensions(canvasRef.value, displaySize);
        });

        isLoaded.value = true;
        loading.value = false;

        readyDialog.value = true;
        setTimeout(() => {
          readyDialog.value = false;
        }, 3000);
      };

      const loop = async () => {
        if (!videoRef.value || !canvasRef.value || !isLoaded.value) return;

        const detections = await faceapi
          .detectAllFaces(videoRef.value, new faceapi.SsdMobilenetv1Options())
          .withFaceLandmarks()
          .withFaceExpressions();

        const resized = faceapi.resizeResults(detections, {
          width: videoRef.value.videoWidth,
          height: videoRef.value.videoHeight,
        });

        const ctx = canvasRef.value.getContext("2d");
        ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height);
        faceapi.draw.drawDetections(canvasRef.value, resized);
        faceapi.draw.drawFaceLandmarks(canvasRef.value, resized);

        if (detections.length > 0) {
          const expressions = detections[0].expressions;
          const top = Object.entries(expressions).sort((a, b) => b[1] - a[1]);
          emotion.value = top[0][0];
        }
      };

      await start();
      const interval = setInterval(loop, 100);

      onUnmounted(() => {
        clearInterval(interval);
      });
    });

    return {
      videoRef,
      canvasRef,
      loading,
      emotion,
      readyDialog,
    };
  },
};
</script>

<style scoped>
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #121212;
  font-family: sans-serif;
}

.main {
  display: flex;
  width: 100%;
  height: 100%;
}

.left-panel, .right-panel {
  width: 50%;
  padding: 20px;
  box-sizing: border-box;
  position: relative;
}

video {
  width: 100%;
  height: auto;
  border-radius: 10px;
  display: block;
}

canvas {
  position: absolute;
  top: 20px;
  left: 20px;
  width: calc(100% - 40px);
  height: auto;
  pointer-events: none;
  border-radius: 10px;
}

.right-panel {
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #1e1e1e;
  border-left: 2px solid #333;
}

.right-panel h3 {
  font-size: 28px;
  margin-bottom: 10px;
  font-weight: bold;
}

.emotion-result {
  font-size: 24px;
  color: #ffeb3b;
  font-weight: 600;
}

/* Modal Styles */
.modal {
  position: absolute;
  z-index: 999;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: #222;
  color: #fff;
  padding: 25px 40px;
  border-radius: 12px;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.modal.ready .modal-content.success {
  background-color: #2e7d32;
  color: #fff;
}
</style>
