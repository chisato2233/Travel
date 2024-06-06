import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import ProfilePage from '../components/ProfilePage.vue';
import Register from '../components/Register.vue';
import HomePage from '../components/HomePage.vue';
import Travel from '../components/Travel.vue';
import Diary from '../components/Diary.vue';
import CreateDiary from '../components/CreateDiary.vue';
import UpdateDiary from '../components/UpdateDiary.vue';
import Recommendations from '../components/Recommendations.vue';
import NotFound from '../components/NotFound.vue';
import DiaryList from '../components/DiaryList.vue';
import AllDiary from '../components/AllDiary.vue';
import AllLocations from '../components/AllLocations.vue'; // Add this line
import AllNodes from '../components/AllNodes.vue'; // Add this line

import VideoListView from '../views/AIGC/VideoListView.vue';

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
    path: '/diarylist',
    name: 'DiaryList',
    component: DiaryList
  },
  {
    path: '/all-diaries',
    name: 'AllDiary',
    component: AllDiary
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
    path: '/create-diary',
    name: 'CreateDiary',
    component: CreateDiary
  },
  {
    path: '/update-diary/:id',
    name: 'UpdateDiary',
    component: UpdateDiary
  },
  {
    path: '/aigc-vedio',
    name: 'VideoList',
    component: VideoListView,
  },
  // Add the routes for AllLocations and AllNodes
  {
    path: '/all-locations',
    name: 'AllLocations',
    component: AllLocations
  },
  {
    path: '/all-nodes',
    name: 'AllNodes',
    component: AllNodes
  },
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
