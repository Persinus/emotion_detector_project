<template>
  <div class="home">
    <div class="content-wrapper">
      <!-- Left Column (Video Section) -->
      <div class="left-column">
        <VideoSection />
      </div>

      <!-- Right Column (Project Details) -->
      <div class="right-column">
        <ProjectDetails />
      </div>
    </div>
  </div>
</template>

<script>
import VideoSection from "../components/VideoSection.vue";
import ProjectDetails from "../components/ProjectDetails.vue";

export default {
  name: "Home",
  components: {
    VideoSection,
    ProjectDetails,
  },
};
</script>

<style scoped>
/* Home container */
.home {
  font-family: 'Arial', sans-serif;
  color: #4a4a4a;
  background-color: #f7f7f7;
  padding: 20px;
}

/* Main content wrapper with 2 columns */
.content-wrapper {
  display: flex;
  flex-wrap: wrap; /* Để hỗ trợ responsive */
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Left column for Video Section */
.left-column {
  flex: 1; /* Chiếm 50% chiều rộng */
  min-width: 300px; /* Đảm bảo chiều rộng tối thiểu trên màn hình nhỏ */
  max-width: 600px; /* Giới hạn chiều rộng tối đa */
}

/* Right column for Project Details */
.right-column {
  flex: 1; /* Chiếm 50% chiều rộng */
  min-width: 300px; /* Đảm bảo chiều rộng tối thiểu trên màn hình nhỏ */
  padding: 20px;
  background: linear-gradient(135deg, #eaf2f8, #c8e1f9); /* Màu nền gradient nhẹ */
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1); /* Bóng nhẹ cho khung */
}
</style>