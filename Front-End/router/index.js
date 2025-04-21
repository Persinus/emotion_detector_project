import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../src/views/Home.vue'),
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('../src/views/Test.vue'),
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Dùng import.meta.env thay vì process.env
  routes
});
export default router;