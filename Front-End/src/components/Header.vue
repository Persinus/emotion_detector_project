<template>
    <header class="header">
      <div class="logo-container">
        <img class="logo" src="../assets/logo.png" alt="Logo" />
        <h1 class="site-title">Deep Learning Emotion Recognition</h1>
      </div>
  
      <!-- Navigation -->
      <nav class="nav">
        <el-menu :default-active="activeMenu" class="el-menu" mode="horizontal" background-color="#42b883" text-color="#ffffff" active-text-color="#d3ffdb">
          <el-menu-item index="1">
            <router-link to="/" class="nav-link">Home</router-link>
          </el-menu-item>
          <el-menu-item index="2">
            <router-link to="/CheckImg" class="nav-link">CheckImage</router-link>
          </el-menu-item>
          <el-menu-item index="3">
            <router-link to="/CheckWebCam" class="nav-link">CheckWebCam</router-link>
          </el-menu-item>
          <el-menu-item index="3">
            <router-link to="/Audio" class="nav-link">CheckAudio</router-link>
          </el-menu-item>
        </el-menu>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: "Header",
    data() {
      return {
        activeMenu: "1", // Menu mặc định được kích hoạt
      };
    },
  };
  </script>
  
  <style scoped>
  .header {
    position: sticky; /* Giữ header dính vào đầu trang khi cuộn */
    top: 0; /* Dính vào phía trên của viewport */
    z-index: 1000; /* Đảm bảo header luôn nằm trên các thành phần khác */
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5em 0.5em; /* Giảm padding để header nhỏ hơn */
    background-color: #42b883; /* Màu xanh Vue.js */
    color: white;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Bóng nhẹ */
    height: 50px; /* Giảm chiều cao header */
    margin: 0; /* Đảm bảo không có khoảng cách xung quanh */
  }
  
  /* Logo và tiêu đề */
  .logo-container {
    display: flex;
    align-items: center;
  }
  
  .logo {
    height: 40px; /* Giảm chiều cao logo */
    margin-right: 1em;
    transition: transform 300ms;
    box-shadow: 0 2px 8px rgba(66,184,131,0.10);
  }
  
  .logo:hover {
    transform: scale(1.1);
  }
  
  .site-title {
    font-size: 1.2rem; /* Giảm kích thước chữ */
    font-weight: bold;
  }
  
  /* Navigation */
  .nav {
    display: flex;
    margin-left: auto;
    align-items: center;
    justify-content: center;
  
    margin-right: 1em; /* Thêm khoảng cách bên phải */
  }
  
  .el-menu {
    background-color: transparent; /* Làm menu trong suốt */
    border: none; /* Loại bỏ đường viền mặc định */
    transition: background 0.3s, color 0.3s, box-shadow 0.3s;
    width: 100%;
    justify-content: flex-start;
  }
  
  .nav-link {
    color: inherit; /* Sử dụng màu chữ mặc định */
    text-decoration: none;
    font-size: 1rem; /* Giảm kích thước chữ */
    padding: 0.5em 1em; /* Thêm khoảng cách xung quanh chữ */
    transition: color 300ms; /* Thêm hiệu ứng chuyển màu khi hover */
    transition: background 0.3s, color 0.3s, box-shadow 0.3s;
  }
  
  .nav-link:hover {
    color: #ffffffcc; /* Màu trắng nhạt khi hover */
    text-decoration: underline; /* Gạch chân khi hover */
    background: rgba(255,255,255,0.08);
    box-shadow: 0 2px 8px rgba(66,184,131,0.10);
  }
  
  .el-menu-item:hover {
    background: rgba(255,255,255,0.08);
    color: #d3ffdb !important;
    box-shadow: 0 2px 8px rgba(66,184,131,0.10);
  }
  
  .el-menu-item:active,
  .nav-link:active {
    background: rgba(66,184,131,0.25);
    color: #fff !important;
  }
  
  /* Đảm bảo header luôn liền mạch với nội dung */
  body {
    margin: 0;
    padding: 0;
  }
  
  /* Responsive: co lại trên màn hình nhỏ */
  @media (max-width: 700px) {
    .header {
      flex-direction: column;
      height: auto;
      padding: 0.5em 0.2em;
      align-items: flex-start;
    }
    .logo-container {
      margin-bottom: 0.5em;
      justify-content: center;
      width: 100%;
    }
    .site-title {
      font-size: 1rem;
    }
    .nav {
      width: 100%;
      justify-content: flex-start;
      margin-right: 0;
    }
    .el-menu {
      width: 100%;
      justify-content: flex-start;
    }
  }
  </style>