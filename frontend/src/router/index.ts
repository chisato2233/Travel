import { createRouter, createWebHistory } from 'vue-router';
import Travel from '../components/Travel.vue';
import Login from '../components/Login.vue';
import HomePage from '../components/HomePage.vue'
//import Diary from '../components/Diary.vue'; // Import Diary component

const routes  = [
   {
    path: '/',
    name: 'Main',
    component: HomePage
  },
  {
    path: '/travel',
    name: 'Travel',
    component: Travel
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  // {
  //   path: '/diary',
  //   name: 'Diary',
  //   component: Diary
  // }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;


