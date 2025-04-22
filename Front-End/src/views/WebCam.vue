<template>
    <div class="webcam-container">
      <h1 class="title">Webcam Demo</h1>
      <div class="video-container">
        <video ref="video" width="640" height="480" autoplay></video>
      </div>
      <div class="button-container">
        <button @click="startWebcam" class="start-button">Mở Webcam</button>
        <button @click="stopWebcam" class="stop-button">Tắt Webcam</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        stream: null,
      };
    },
    methods: {
      async startWebcam() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          try {
            this.stream = await navigator.mediaDevices.getUserMedia({
              video: true,
            });
            this.$refs.video.srcObject = this.stream;
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
          tracks.forEach(track => track.stop());
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .webcam-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f8f9fa;
    min-height: 100vh;
    padding: 20px;
  }
  
  .title {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 20px;
  }
  
  .video-container {
    margin-bottom: 20px;
    border: 2px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
  }
  
  video {
    border-radius: 8px;
  }
  
  .button-container {
    display: flex;
    gap: 20px;
  }
  
  button {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
  }
  
  .start-button {
    background-color: #4CAF50;
    color: white;
  }
  
  .start-button:hover {
    background-color: #45a049;
  }
  
  .stop-button {
    background-color: #f44336;
    color: white;
  }
  
  .stop-button:hover {
    background-color: #e53935;
  }
  </style>
  