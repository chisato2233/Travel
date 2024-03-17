import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../components/UserLogin.vue'; // 调整路径以匹配您的文件结构

// 定义路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: UserLogin,
  },
  // 定义其他路由规则...
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
