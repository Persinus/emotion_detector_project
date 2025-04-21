import { createApp } from 'vue'

import App from './App.vue'
import router from '../router' // Import đúng từ ./router

const app = createApp(App)
app.use(router)    // Kích hoạt Vue Router để quản lý các route trong ứng dụng
app.mount('#app')
