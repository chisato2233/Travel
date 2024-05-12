import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'; // 确保导入了 store

createApp(App).use(store).use(router).mount('#app')
