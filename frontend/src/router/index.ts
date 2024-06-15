import { createRouter, createWebHistory } from 'vue-router';
import axios from 'axios';

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

router.beforeEach(async (to, from, next) => {
  if (to.path === '/profile') {
    if (!await isLoggedIn()) {
      next({ name: 'Login' });
    } else {
      next();
    }
  } else if (to.meta.requiresAuth && !await isLoggedIn()) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

async function isLoggedIn() {
  // try {
  //   const response = await axios.get('http://localhost:8000/api/users/check-auth', {
  //     headers: {
  //       Authorization: `Bearer ${localStorage.getItem('token')}`
  //     }
  //   });
    
  //   return response.data.isLoggedIn;
  // } catch (error) {
  //   console.error('检查用户登录状态失败:', error);
  //   return false;
  // }
    try {
    const response = await axios.get('http://localhost:8000/api/users/user/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    if (response.status === 200) {
      console.log('用户已登录');
      return true;
    }
  } catch (error) {
    console.error('用户未登录:', error);
    return false;
  }
}

export default router;
