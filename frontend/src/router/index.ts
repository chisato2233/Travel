import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Travel from '../components/Travel.vue';
import Login from '../components/Login.vue';
import Diary from '../components/Diary.vue'; // Import Diary component

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Travel',
    component: Travel
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/diary',
    name: 'Diary',
    component: Diary
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;


