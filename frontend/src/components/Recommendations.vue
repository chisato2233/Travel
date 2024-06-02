<template>
  <div class="recommendation-container">
    <div class="header">
      <h2>推荐目的地</h2>
      <button class="search-button" @click="navigateToSearch">
        🔍
      </button>
    </div>

    <div v-if="isLoading" class="loading">加载中...</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div v-if="!isLoading && recommendations.length" class="recommendations">
      <div v-for="destination in recommendations" :key="destination.id" class="destination-card">
        <div class="destination-info">
          <h3>{{ destination.name }}</h3>
          <p>{{ destination.description }}</p>
          <p>评分: {{ destination.rating }} / 人气: {{ destination.popularity }}</p>
        </div>
      </div>
    </div>

    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件

const recommendations = ref([]);
const isLoading = ref(true);
const errorMessage = ref('');
const router = useRouter();
const token = localStorage.getItem('token');

const fetchRecommendations = async () => {
  try {
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

onMounted(fetchRecommendations);
</script>

<style scoped>
.recommendation-container {
  width: 80%;
  margin: auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  margin: 0;
}

.search-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.loading {
  text-align: center;
  font-size: 18px;
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
  border: 1px solid #ccc;
  border-radius: 10px;
  margin: 10px;
  padding: 15px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
}

.destination-card:hover {
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}

.destination-info {
  text-align: left;
}

.destination-info h3 {
  margin: 0 0 10px;
}

.destination-info p {
  margin: 5px 0;
}
</style>
