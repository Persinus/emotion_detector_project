<template>
  <div class="home">
    <div class="content-wrapper">
      <div class="left-column">
        <!-- Video -->
        <div class="video-container animate__animated animate__fadeInLeft">
          <iframe
            class="video-frame"
            src="https://www.youtube.com/embed/YOUR_VIDEO_ID"
            frameborder="0"
            allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          ></iframe>
          <!-- Mô tả video -->
          <div class="video-description">
            <p class="video-text">Video này là bản demo minh họa cách hệ thống nhận diện cảm xúc hoạt động dựa trên Deep Learning.</p>
            <router-link to="/test" class="test-button">Chuyển đến Chạy thử</router-link>
          </div>
        </div>
      </div>
      <div class="right-column">
        <!-- Tên dự án -->
        <h1 class="main-title animate__animated animate__fadeInDown">Dự Án Deep Learning: Nhận Diện Cảm Xúc Qua Hình Ảnh</h1>
        <!-- Giới thiệu nhóm -->
        <div class="team-info animate__animated animate__fadeInUp">
          <h2 class="section-title">Nhóm thực hiện: Chaos</h2>
          <ul class="team-list">
            <li>122001472-Nguyễn Văn Mạnh</li>
            <li>122000472-Lê Phúc Hậu</li>
          </ul>
        </div>
        <!-- Giới thiệu FER-2013 -->
        <div class="project-info animate__animated animate__fadeInUp">
          <h2 class="section-title">Giới thiệu FER-2013:</h2>
          <p>
            FER-2013 (Facial Expression Recognition 2013) là tập dữ liệu tiêu chuẩn được sử dụng trong các bài toán nhận diện cảm xúc. 
            Tập dữ liệu này bao gồm hơn 35.000 hình ảnh đen trắng kích thước 48x48 pixel được gán nhãn với các cảm xúc như Hạnh phúc, Buồn, Ngạc nhiên, Tức giận, và nhiều cảm xúc khác.
          </p>
          <p>
            Trong dự án này, chúng tôi áp dụng các kỹ thuật Deep Learning để phân tích và nhận diện cảm xúc từ hình ảnh dựa trên tập dữ liệu FER-2013.
          </p>
        </div>
        <!-- Cảm ơn -->
        <p class="thank-you animate__animated animate__fadeInUp">Cảm ơn bạn đã ghé thăm dự án của chúng tôi!</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>

<style scoped>
/* Tổng thể */
.home {
  font-family: 'Arial', sans-serif;
  color: #4a4a4a;
  background-color: #f7f7f7;
  padding: 40px 20px;
}

/* Bố cục chính */
.content-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Video bên trái */
.left-column {
  flex: 1.2;
  min-width: 350px;
  max-width: 700px;
}

.video-container {
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.video-frame {
  width: 100%;
  height: 450px;
  border: none;
}

/* Mô tả video */
.video-description {
  margin-top: 20px;
  text-align: center;
  font-size: 1rem;
  color: #555;
}

.video-text {
  margin-bottom: 15px;
}

.test-button {
  display: inline-block;
  margin-top: 30px; /* Tăng khoảng cách để nút dịch chuyển xuống */
  padding: 12px 25px;
  background: #add8e6; /* Thay đổi nền thành màu xanh lam nhạt */
  color: white;
  text-decoration: none;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: bold;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 10px rgba(173, 216, 230, 0.5); /* Điều chỉnh bóng để phù hợp với màu nền */
}

.test-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 15px rgba(173, 216, 230, 0.7); /* Điều chỉnh bóng khi hover */
}

/* Nội dung bên phải */
.right-column {
  flex: 1.5;
  min-width: 300px;
  padding: 20px;
  background: linear-gradient(135deg, #eaf2f8, #c8e1f9);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

/* Tiêu đề chính */
.main-title {
  font-size: 2.7rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #2c3e50;
  text-align: center;
}

/* Tiêu đề phụ */
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 10px;
}

/* Danh sách nhóm */
.team-info {
  margin-bottom: 20px;
}

.team-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.team-list li {
  font-size: 1.2rem;
  margin-bottom: 5px;
}

/* Giới thiệu dự án */
.project-info {
  margin-bottom: 20px;
}

.project-info p {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 10px;
  color: #4a4a4a;
}

/* Cảm ơn */
.thank-you {
  font-size: 1.2rem;
  font-style: italic;
  text-align: center;
  color: #555;
  margin-top: 20px;
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }

  .video-frame {
    height: 280px;
  }

  .main-title {
    font-size: 2.2rem;
  }

  .section-title {
    font-size: 1.3rem;
  }

  .project-info p,
  .team-list li {
    font-size: 1rem;
  }

  .test-button {
    font-size: 1rem;
    padding: 10px 20px;
  }
}
</style>
