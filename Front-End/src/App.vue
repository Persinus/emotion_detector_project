<script setup>
// Không cần nội dung trong <script setup> nếu bạn chỉ cần render router-view và hiệu ứng logo
</script>

<template>
  <div class="app-container">
    <!-- Đảm bảo rằng logo được đặt trong một phần tử có class 'logo' -->
    <img class="logo" src="./Front-End/src/assets/logo.png" alt="Logo" />
    <!-- router-view sẽ hiển thị các thành phần tương ứng với route -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
/* Hiệu ứng hover trên logo */
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

/* Nếu bạn muốn sử dụng các hiệu ứng khác cho logo trong các thành phần khác nhau */
.logo.some-other-class:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>