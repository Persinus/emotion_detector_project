<template>
  <el-card class="video-card animate__animated animate__fadeInLeft">
    <!-- Tiêu đề chính -->
    <va-card class="main-card animate__animated animate__fadeInDown">
      <h1 class="main-title">Dự Án Deep Learning: Nhận Diện Cảm Xúc Qua Hình Ảnh</h1>
    </va-card>

    <!-- Mô tả video -->
    <div class="video-description">
      <p class="video-text">
        Video này là bản demo minh họa cách hệ thống nhận diện cảm xúc hoạt động dựa trên Deep Learning.
      </p>
    </div>

    <!-- Video -->
    <div class="video-container">
      <iframe
        class="video-frame"
        src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
        frameborder="0"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </el-card>
</template>

<script>
export default {
  name: "VideoSection",
};
</script>

<style scoped>
/* Tổng thể */
.video-card {

border-radius: 12px;
box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Bóng nhẹ */

text-align: center; /* Căn giữa nội dung */
}

/* Tiêu đề chính */
.main-title {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50; /* Màu chữ đậm */
  margin-bottom: 20px;
}

/* Container video */
.video-container {
  margin: 20px auto; /* Căn giữa video */
  max-width: 800px; /* Giới hạn chiều rộng video */
}

.video-frame {
  width: 100%; /* Video full width trong container */
  height: 450px; /* Chiều cao cố định */
  border: none;
  border-radius: 12px; /* Bo tròn góc video */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Bóng nhẹ cho video */
}

/* Mô tả video */
.video-description {
  margin-top: 20px;
  font-size: 1.2rem; /* Kích thước chữ lớn hơn */
  line-height: 1.8; /* Khoảng cách dòng rộng hơn */
  color: #555; /* Màu chữ xám */
  max-width: 800px; /* Giới hạn chiều rộng mô tả */
  margin-left: auto;
  margin-right: auto;
}

/* Văn bản mô tả */
.video-text {
  margin-bottom: 15px;
  color: #4a4a4a; /* Màu chữ đậm hơn */
}

/* Nút bấm (nếu cần thêm sau này) */
.test-button {
  font-size: 1rem;
  font-weight: bold;
  margin-top: 20px;
  padding: 10px 20px;
  border-radius: 20px; /* Nút tròn mềm mại */
  background-color: #42b883; /* Màu nền nút */
  color: white; /* Màu chữ */
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.test-button:hover {
  background-color: #2c3e50; /* Màu nền khi hover */
  color: #fff; /* Màu chữ khi hover */
  transform: scale(1.05); /* Hiệu ứng phóng to nhẹ */
}
</style>