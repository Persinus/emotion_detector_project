<template>
  <div class="project-details">
    <!-- Title Section -->
    

    <!-- Team Info Section -->
    <va-card class="team-card animate__animated animate__fadeInUp">
      <h2 class="section-title">Nhóm thực hiện</h2>
      <el-list class="team-list">
        <el-list-item>
          <el-avatar icon="el-icon-user" size="medium" />
          <span class="team-member">122001472 - Nguyễn Văn Mạnh</span>
        </el-list-item>
        <el-list-item>
          <el-avatar icon="el-icon-user" size="medium" />
          <span class="team-member">122000472 - Lê Phúc Hậu</span>
        </el-list-item>
      </el-list>
    </va-card>

    <!-- Project Info Section -->
    <va-card class="project-card animate__animated animate__fadeInUp">
      <h2 class="section-title">Giới thiệu FER-2013</h2>
      <div class="project-info">
        <p>
          FER-2013 (Facial Expression Recognition 2013) là tập dữ liệu tiêu chuẩn được sử dụng trong các bài toán nhận diện cảm xúc.
          Tập dữ liệu này bao gồm hơn 35.000 hình ảnh đen trắng kích thước 48x48 pixel được gán nhãn với các cảm xúc như Hạnh phúc, Buồn, Ngạc nhiên, Tức giận, và nhiều cảm xúc khác.    
          Trong dự án này, chúng tôi áp dụng các kỹ thuật Deep Learning để phân tích và nhận diện cảm xúc từ hình ảnh dựa trên tập dữ liệu FER-2013.
        </p>
      </div>
    </va-card>
  </div>
</template>

<script>
export default {
  name: "ProjectDetails",
};
</script>

<style scoped>
/* Tổng quan */
.project-details {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px; /* Khoảng cách giữa các thẻ */
  max-width: 900px; /* Tăng chiều rộng tối đa */
  margin: 0 auto; /* Căn giữa container */
}



/* Tiêu đề từng phần */
.section-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 15px;
  text-align: center; /* Căn giữa tiêu đề */
}

/* Thẻ nhóm thực hiện */
.team-card {
  border-radius: 12px;
  background-color: #f9fafb; /* Màu nền nhẹ */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.team-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.el-list-item {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 1.2rem;
  color: #2c3e50;
}

.team-member {
  word-wrap: break-word; /* Đảm bảo chữ không bị tràn */
}

.el-avatar {
  background-color: #42b883; /* Màu nền avatar */
  color: white;
}

/* Thẻ thông tin dự án */
.project-card {
  border-radius: 12px;
  background-color: #ffffff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  font-size: 1.1rem;
  color: #4a4a4a;
  line-height: 1.8; /* Tăng khoảng cách dòng */
}

.project-info p {
  margin-bottom: 15px;
  text-align: justify;
  word-wrap: break-word; /* Đảm bảo chữ không bị tràn */
}

/* Card bóng đẹp */
.va-card {
  box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.15);
}
</style>
