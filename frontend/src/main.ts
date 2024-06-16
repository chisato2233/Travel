// src/main.ts

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store'; // 确保导入了 store
 // 导入插件
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

const app = createApp(App);

app.use(store);
app.use(router);

app.mount('#app');
