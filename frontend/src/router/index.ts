import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import ProfilePage from '../components/ProfilePage.vue';
import Register from '../components/Register.vue';
import HomePage from '../components/HomePage.vue';
import Travel from '../components/Travel.vue';
import Diary from '../components/Diary.vue';
import CreateDiary from '../components/CreateDiary.vue'; // 引入CreateDiary组件
import UpdateDiary from '../components/UpdateDiary.vue'; // 引入UpdateDiary组件
import Recommendations from '../components/Recommendations.vue';
import NotFound from '../components/NotFound.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/notfound',
    name: 'NotFound',
    component: NotFound
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: Recommendations
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/profile',
    name: 'ProfilePage',
    component: ProfilePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/travel',
    name: 'Travel',
    component: Travel
  },
  {
    path: '/diary',
    name: 'Diary',
    component: Diary,
    meta: { requiresAuth: true }
  },
  {
    path: '/create-diary', // 设置CreateDiary.vue的路由路径
    name: 'CreateDiary',
    component: CreateDiary
  },
  {
    path: '/update-diary/:id', // 修改路由路径，接收日记ID作为参数
    name: 'UpdateDiary',
    component: UpdateDiary
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !token) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

export default router;
