<template>
  <div class="recommendation-container">
    <div class="header">
      <h2>推荐目的地</h2>
      <div class="button-group">
        <button class="nav-button" @click="navigateToAllLocations">
          <i class="fas fa-map-marker-alt"></i>
        </button>
        <button class="nav-button" @click="navigateToAllNodes">
          <i class="fas fa-network-wired"></i>
        </button>
        <button class="nav-button" @click="navigateToSearch">
          <i class="fas fa-search"></i>
        </button>
        <button class="nav-button" @click="navigateToAIGCVideo">
          <i class="fas fa-video"></i>
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading">加载中...</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <transition name="fade" mode="out-in">
      <div v-if="!isLoading && recommendations.length" class="recommendations">
        <div v-for="destination in recommendations" :key="destination.id" class="destination-card"
          @click="navigateToTravel">
          <div class="destination-info">
            <h3>{{ destination.name }}</h3>
            <p>{{ destination.description }}</p>
            <p>评分: {{ destination.rating }} / 人气: {{ destination.popularity }}</p>
            <p v-if="destination.interests && destination.interests.length">兴趣: {{ destination.interests.join(', ') }}
            </p>
          </div>
        </div>
      </div>
    </transition>

    <!-- 登录组件 -->
    <Login v-if="!isLoggedIn && showLogin" @close="handleLoginClose" />

    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Navbar from './Navbar.vue';
import Login from './Login.vue';

const recommendations = ref([]);
const isLoading = ref(true);
const errorMessage = ref('');
const router = useRouter();

const token = localStorage.getItem('token');

const isLoggedIn = ref(!!token);
const showLogin = ref(false);
const manualLoginClose = ref(false);

const openLogin = () => {
  if (!manualLoginClose.value && !isLoggedIn.value) {
    showLogin.value = true;
  }
};

const handleLoginClose = () => {
  showLogin.value = false;
  manualLoginClose.value = true;
};

watch(isLoggedIn, (newValue) => {
  if (newValue) {
    handleLoginClose();
  }
});

onMounted(() => {
  setTimeout(() => {
    openLogin();
  }, 5000);
});

const fetchRecommendations = async () => {
  try {
    const token = localStorage.getItem('token');

    const response = await axios.get('http://localhost:8000/api/recommendations/destinations/', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        popularity: 1000
      }
    });
    recommendations.value = response.data;
  } catch (error) {
    console.error('获取推荐目的地失败:', error);
    if (error.response && error.response.status === 400) {
      errorMessage.value = error.response.data.error || 'Invalid query parameters.';
    } else {
      errorMessage.value = '获取推荐目的地失败，请稍后重试。';
    }
  } finally {
    isLoading.value = false;
  }
};

const navigateToSearch = () => {
  router.push({ name: 'HomePage' });
};

const navigateToTravel = () => {
  router.push({ name: 'Travel' });
};

const navigateToAllLocations = () => {
  router.push({ name: 'AllLocations' });
};

const navigateToAllNodes = () => {
  router.push({ name: 'AllNodes' });
};

const navigateToAIGCVideo = () => {
  router.push({ name: 'VideoList' });
};

onMounted(fetchRecommendations);
</script>

<style scoped>
.recommendation-container {
  width: 80%;
  margin: auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
}

h2 {
  margin: 0;
  color: #333;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

.recommendations {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.destination-card {
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 10px;
  margin: 10px;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s, transform 0.3s, border-color 0.3s;
  cursor: pointer;
}

.destination-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
  border-color: #007bff;
}

.destination-info {
  text-align: left;
}

.destination-info h3 {
  margin: 0 0 10px;
  color: #007bff;
}

.destination-info p {
  margin: 5px 0;
  color: #555;
}

/* 按钮样式 */
.nav-button,
.search-button,
.aigc-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s, transform 0.3s;
}

.nav-button i,
.search-button i,
.aigc-button i {
  margin: 0;
}

.nav-button:hover,
.search-button:hover,
.aigc-button:hover {
  background-color: #45a049;
  transform: scale(1.1);
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
