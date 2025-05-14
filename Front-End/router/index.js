import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../src/views/Home.vue'),
  },
  {
    path: '/CheckImg',
    name: 'Test',
    component: () => import('../src/views/CheckImg.vue'),
  },
  {
    path: '/CheckWebCam',
    name: 'Testcam',
    component: () => import('../src/views/CheckVideo.vue'),
  },
  //
  {
    path: '/Audio',
    name: 'Audio',
    component: () => import('../src/views/Audio.vue'),
  }
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Dùng import.meta.env thay vì process.env
  routes
});
export default router;