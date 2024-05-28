import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import ProfilePage from '../components/ProfilePage.vue';
import Register from '../components/Register.vue';
import HomePage from '../components/HomePage.vue';
import Travel from '../components/Travel.vue';
import Diary from '../components/Diary.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
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