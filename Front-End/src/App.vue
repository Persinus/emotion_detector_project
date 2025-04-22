<script setup>
// Import Header component
import Header from "./components/Header.vue";
</script>

<template>
  <Header />
  <div class="app-container">
    <!-- Header xuất hiện trên tất cả các trang -->
   
    <!-- Nội dung thay đổi theo route -->
    <router-view />
  </div>
</template>

<style scoped>
.app-container {
  font-family: Arial, sans-serif;
  color: #333;
  background-color: #f9f9f9;

  display: flex;
  flex-direction: column;
}
</style>
