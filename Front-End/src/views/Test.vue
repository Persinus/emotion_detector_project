<template>
  <div class="container mt-5">
    <!-- Header -->
    <header class="text-center mb-4">
      <h1 class="title">Upload Ảnh để Nhận Diện Cảm Xúc</h1>
      <button
        class="btn btn-primary btn-lg"
        @click="toggleInstructions"
      >
        Hướng Dẫn
      </button>
    </header>

    <!-- Stepper Panel -->
    <transition name="fade">
      <div v-if="showInstructions" class="stepper-panel animate__animated animate__fadeIn">
        <h3 class="text-secondary mb-4">Hướng Dẫn Upload Ảnh</h3>
        <div class="steps">
          <div
            class="step"
            :class="{ active: currentStep === step.id }"
            v-for="step in steps"
            :key="step.id"
            @click="goToStep(step.id)"
          >
            <div class="circle">{{ step.id }}</div>
            <span>{{ step.label }}</span>
          </div>
        </div>
        <p class="step-content">{{ getStepContent() }}</p>
      </div>
    </transition>

    <!-- Main Layout -->
    <div class="row">
      <!-- Left: Upload Image -->
      <div class="col-md-6 upload-section">
        <h4>Chọn Ảnh</h4>
        <input
          type="file"
          class="form-control mb-3"
          @change="handleFileUpload"
          accept=".jpg, .jpeg, .png"
        />
        <button
          class="btn btn-success w-100"
          :disabled="!selectedImage"
          @click="submitImage"
        >
          Nhận Diện Cảm Xúc
        </button>

        <transition name="fade">
          <div v-if="loading" class="text-center mt-3">
            <div class="spinner-border text-primary"></div>
            <p class="mt-2">Đang xử lý...</p>
          </div>
        </transition>
      </div>

      <!-- Right: Display Result -->
      <div class="col-md-6 result-section">
        <h4>Kết Quả</h4>
        <div v-if="selectedImagePreview" class="image-preview mb-3">
          <img
            :src="selectedImagePreview"
            alt="Ảnh đã chọn"
            class="img-fluid rounded"
          />
        </div>
        <transition name="fade">
          <div v-if="result" class="result-list">
            <ul class="list-group">
              <li
                v-for="(score, label) in result"
                :key="label"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                {{ label }}
                <span class="badge bg-primary">{{ (score * 100).toFixed(2) }}%</span>
              </li>
            </ul>
          </div>
        </transition>
        <button
          v-if="selectedImage"
          class="btn btn-secondary w-100 mt-3"
          @click="resetUpload"
        >
          Chọn Ảnh Khác
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "EmotionDetection",
  data() {
    return {
      selectedImage: null,
      selectedImagePreview: null,
      result: null,
      loading: false,
      showInstructions: false,
      currentStep: 1,
      steps: [
        { id: 1, label: "Chọn ảnh" },
        { id: 2, label: "Kiểm tra kích thước" },
        { id: 3, label: "Kiểm tra định dạng" },
        { id: 4, label: "Upload" },
      ],
    };
  },
  methods: {
    toggleInstructions() {
      this.showInstructions = !this.showInstructions;
    },
    goToStep(stepId) {
      this.currentStep = stepId;
    },
    getStepContent() {
      switch (this.currentStep) {
        case 1:
          return "Chọn một ảnh từ thiết bị của bạn.";
        case 2:
          return "Đảm bảo ảnh có kích thước 48x48 pixel.";
        case 3:
          return "Ảnh phải có định dạng JPG/PNG và màu đen trắng.";
        case 4:
          return "Nhấn nút 'Nhận Diện Cảm Xúc' để gửi ảnh lên.";
        default:
          return "";
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedImage = file;
        this.selectedImagePreview = URL.createObjectURL(file);
      }
    },
    async submitImage() {
      if (!this.selectedImage) return;

      this.loading = true;
      this.result = null;

      const formData = new FormData();
      formData.append("image", this.selectedImage);

      try {
        const response = await axios.post(
          "https://your-backend-url/api/predict",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );
        this.result = response.data;
      } catch (error) {
        console.error("Lỗi khi gửi ảnh:", error);
      } finally {
        this.loading = false;
      }
    },
    resetUpload() {
      this.selectedImage = null;
      this.selectedImagePreview = null;
      this.result = null;
    },
  },
};
</script>
<style scoped>
/* Tổng quan */
.container {
  max-width: 900px;
  margin: auto;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #0d6efd;
}

/* Stepper Panel */
.stepper-panel {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f8f9fa;
  margin-bottom: 2rem;
}

.steps {
  display: flex;
  justify-content: space-between;
}

.step {
  text-align: center;
  cursor: pointer;
}

.step .circle {
  width: 40px;
  height: 40px;
  background: #e9ecef;
  border-radius: 50%;
  line-height: 40px;
  font-weight: bold;
  color: #6c757d;
  margin: auto;
  transition: all 0.3s;
}

.step.active .circle {
  background: #0d6efd;
  color: white;
}

.step span {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

/* Left: Upload Section */
.upload-section {
  border-right: 1px solid #ddd;
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
}

/* Right: Result Section */
.result-section {
  text-align: center;
}

.result-list ul {
  list-style: none;
  padding: 0;
}

.result-list li {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f8f9fa;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
