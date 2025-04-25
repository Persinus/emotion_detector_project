<template>
  <div class="research-container">
    <h1>Trang này đang trong quá trình nghiên cứu</h1>
    <p>Vui lòng chờ tôi trong vòng 1 tháng tới.</p>
  </div>
</template>

<script>
export default {
  name: "VanBan",
};
</script>

<style scoped>
.research-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  color: #333;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

p {
  font-size: 1.2rem;
  color: #555;
}
</style>