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
<<<<<<< HEAD
    
    <div v-if="!isLoading && recommendations.length" class="recommendations">
      <div v-for="destination in recommendations" :key="destination.id" class="destination-card" @click="navigateToTravel">
        <img :src="destination.imageURL" :alt="destination.name" class="destination-image">
=======

    <div v-if="!isLoading && recommendations.length" class="recommendations">
      <div v-for="destination in recommendations" :key="destination.id" class="destination-card">
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929
        <div class="destination-info">
          <h3>{{ destination.name }}</h3>
          <p>{{ destination.description }}</p>
          <p>评分: {{ destination.rating }} / 人气: {{ destination.popularity }}</p>
<<<<<<< HEAD
          <p>兴趣: {{ destination.interests.join(', ') }}</p>
        </div>
      </div>
    </div>
    
    <!-- 登录组件 -->
    <Login v-if="!isLoggedIn && showLogin" @close="handleLoginClose" />
=======
        </div>
      </div>
    </div>
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929

    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
<<<<<<< HEAD
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件
import Login from './Login.vue';

// 从 localStorage 中获取令牌，如果不存在则返回 null
const token = localStorage.getItem('token');
=======
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929

const recommendations = ref([]);
const isLoading = ref(true);
const errorMessage = ref('');
const router = useRouter();
<<<<<<< HEAD

// 判断用户是否已经登录，如果已经登录且令牌有效，则不再显示登录界面
const isLoggedIn = ref(!!token);
const showLogin = ref(false); // 初始状态为隐藏登录界面
const manualLoginClose = ref(false); // 标志位，用于跟踪用户是否手动关闭了登录界面

const openLogin = () => {
  if (!manualLoginClose.value && !isLoggedIn.value) { // 仅在用户未手动关闭登录界面且未登录的情况下自动显示
    showLogin.value = true; // 控制显示登录界面
  }
};

const handleLoginClose = () => {
  showLogin.value = false; // 控制隐藏登录界面
  manualLoginClose.value = true; // 设置标志位，表示用户已手动关闭登录界面
};

// 监听用户登录状态的变化，如果用户登录成功，则隐藏登录组件
watch(isLoggedIn, (newValue) => {
  if (newValue) {
    handleLoginClose(); // 登录成功后关闭登录组件
  }
});

// 在进入主页后一段时间后显示登录组件
onMounted(() => {
  setTimeout(() => {
    openLogin();
  }, 5000); // 5秒后显示登录组件
});
=======
const token = localStorage.getItem('token');
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929

const fetchRecommendations = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/recommendations/destinations/', {
<<<<<<< HEAD
      params: {
        popularity: 1000 // 可选参数，设定过滤热门目的地的阈值
=======
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        popularity: 1000
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929
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

<<<<<<< HEAD
const navigateToTravel = () => {
  router.push({ name: 'Travel' });
};

=======
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929
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
<<<<<<< HEAD
  cursor: pointer;
=======
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929
}

.destination-card:hover {
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}

<<<<<<< HEAD
.destination-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
}

=======
>>>>>>> 2cbb457fe86c4b33c21a76fdf33de41b742ac929
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
