import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue'; // 导入登录组件
import ProfilePage from '../components/ProfilePage.vue'; // 导入个人资料页面组件
import Register from '../components/Register.vue'; // 导入注册组件
import HomePage from '../components/HomePage.vue'; // 导入首页组件
import Travel from '../components/Travel.vue'; // 导入寻路页面组件
import Diary from '../components/Diary.vue'; // 导入日记页面组件

const routes = [
  {
    path: '/', // 首页路由路径
    name: 'HomePage', // 路由名称
    component: HomePage // 组件
  },
  {
    path: '/register', // 注册页面路由路径
    name: 'Register', // 路由名称
    component: Register // 组件
  },
  {
    path: '/profile', // 个人资料页面路由路径
    name: 'ProfilePage', // 路由名称
    component: ProfilePage // 组件
  },
  {
    path: '/login', // 登录页面路由路径
    name: 'Login', // 路由名称
    component: Login // 组件
  },
  {
    path: '/travel', // 寻路页面路由路径
    name: 'Travel', // 路由名称
    component: Travel // 组件
  },
  {
    path: '/diary', // 日记页面路由路径
    name: 'Diary', // 路由名称
    component: Diary, // 组件
    meta: { requiresAuth: true } // 添加元信息，表示需要身份验证
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// 导航守卫，用于检查路由是否需要身份验证
router.beforeEach((to, from, next) => {
  if (to.path === '/profile') {
    if (!isLoggedIn()) {
      next({ name: 'Login' }); // 若未登录，则导航到登录页面
    } else {
      next(); // 否则，允许导航到个人资料页面
    }
  } else if (to.meta.requiresAuth && !isLoggedIn()) {
    next({ name: 'Login' }); // 若需要身份验证且未登录，则导航到登录页面
  } else {
    next(); // 其他情况，允许导航
  }
});

// 模拟用户是否已登录的函数
function isLoggedIn() {
  // 假设你有一个方法来检查用户是否已经登录
  // 返回 true 表示用户已登录，否则返回 false
  // 这里可以根据你的实际情况进行调整
  return true; // 假设默认已登录
}

export default router;