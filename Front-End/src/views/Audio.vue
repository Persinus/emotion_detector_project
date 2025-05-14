<template>
  <div class="audio-main-container">
    <div class="audio-left">
      <h2>Hướng dẫn sử dụng</h2>
      <ul>
        <li>Chọn file âm thanh ngắn (dưới 30s, định dạng .mp3).</li>
        <li>Bấm <b>Tải lên</b> để gửi file lên hệ thống.</li>
        <li>Có thể nghe lại file vừa chọn trước khi gửi.</li>
        <li>Kết quả cảm xúc sẽ hiển thị ngay bên dưới.</li>
      </ul>
      <img src="../assets/logo.png" alt="Audio Guide" class="audio-guide-img" />
    </div>
    <div class="audio-right">
      <h1>Tải Lên Tệp Âm Thanh Cảm Xúc</h1>
      <input type="file" @change="onFileChange" accept=".mp3" class="file-input" />
      <button @click="uploadFile" :disabled="!selectedFile || isLoading">
        {{ isLoading ? "Đang tải lên..." : "Tải lên" }}
      </button>
      <audio v-if="audioSrc" :src="audioSrc" controls style="margin-top:12px; width:100%"></audio>
      <p v-if="uploadSuccess" class="success-message">Tải lên thành công!</p>
      <p v-if="audioUrl" class="result">Cảm xúc dự đoán: {{ audioUrl }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "Audio",
  setup() {
    const selectedFile = ref(null);  // Để lưu tệp đã chọn
    const audioUrl = ref(null);  // Để lưu kết quả dự đoán
    const errorMessage = ref(null);  // Để lưu thông báo lỗi
    const isLoading = ref(false);  // Để theo dõi trạng thái tải lên
    const audioSrc = ref(null);  // Để lưu đường dẫn tệp âm thanh
    const uploadSuccess = ref(false);  // Để theo dõi trạng thái thành công

    const onFileChange = (event) => {
      // Lấy tệp đã chọn
      const file = event.target.files[0];
      if (file) {
        selectedFile.value = file;
        errorMessage.value = null;  // Reset thông báo lỗi
        audioSrc.value = URL.createObjectURL(file);  // Tạo đường dẫn tạm cho tệp
      }
    };

    const uploadFile = async () => {
      if (!selectedFile.value) {
        errorMessage.value = "Vui lòng chọn tệp âm thanh!";
        return;
      }

      const formData = new FormData();
      formData.append("file", selectedFile.value);

      isLoading.value = true;
      uploadSuccess.value = false;
      errorMessage.value = null;

      try {
        const response = await fetch("http://localhost:5000/predict_audio", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Lỗi khi gửi tệp âm thanh.");
        }

        const result = await response.json();
        if (result.error) {
          errorMessage.value = `Lỗi: ${result.error}`;
        } else {
          audioUrl.value = result.emotion;
          uploadSuccess.value = true;
        }
      } catch (error) {
        errorMessage.value = `Lỗi: ${error.message}`;
      } finally {
        isLoading.value = false;
      }
    };

    return {
      selectedFile,
      audioUrl,
      errorMessage,
      isLoading,
      audioSrc,
      uploadSuccess,
      onFileChange,
      uploadFile,
    };
  },
};
</script>

<style scoped>
.audio-main-container {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 36px;
  max-width: 900px;
  margin: 40px auto 0 auto;
  background: linear-gradient(120deg, #e0f7fa 60%, #f9f9f9 100%);
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(0,123,255,0.07);
  padding: 32px 18px;
}
.audio-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 18px 12px;
  box-shadow: 0 2px 8px rgba(0,123,255,0.06);
}
.audio-left h2 {
  color: #007bff;
  margin-bottom: 10px;
}
.audio-left ul {
  text-align: left;
  color: #333;
  font-size: 1.05rem;
  margin-bottom: 18px;
  padding-left: 18px;
}
.audio-guide-img {
  width: 90px;
  opacity: 0.85;
  margin-top: 12px;
}
.audio-right {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 18px 16px;
  box-shadow: 0 2px 8px rgba(0,123,255,0.06);
}
h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #007bff;
  letter-spacing: 1px;
  animation: fadeInDown 0.7s;
}
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-30px);}
  50% { opacity: 0.5; transform: translateY(-15px);}
  to { opacity: 1; transform: translateY(0);}
}
.file-input {
  margin: 10px;
  padding: 6px;
  border-radius: 6px;
  border: 1px solid #b2ebf2;
  background: #fff;
  transition: border 0.3s;
}
.file-input:focus {
  border: 1.5px solid #007bff;
}
button {
  padding: 10px 24px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  background: linear-gradient(90deg, #007bff 60%, #00bcd4 100%);
  color: white;
  margin-top: 8px;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(0,123,255,0.08);
}
button:hover:not(:disabled) {
  background: linear-gradient(90deg, #0056b3 60%, #0097a7 100%);
  transform: translateY(-2px) scale(1.04);
  box-shadow: 0 4px 16px rgba(0,123,255,0.13);
}
button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.result {
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
.success-message {
  color: #4caf50;
  font-weight: bold;
  margin-top: 1rem;
  animation: fadeIn 1s;
}
@keyframes shake {
  10%, 90% { transform: translateX(-2px);}
  20%, 80% { transform: translateX(4px);}
  30%, 50%, 70% { transform: translateX(-8px);}
  40%, 60% { transform: translateX(8px);}
}
/* Responsive */
@media (max-width: 900px) {
  .audio-main-container {
    flex-direction: column;
    padding: 12px 2vw;
    max-width: 99vw;
    gap: 18px;
  }
  .audio-left, .audio-right {
    padding: 12px 6px;
  }
  .audio-guide-img {
    width: 60px;
  }
}
</style>
