<template>
  <div class="home-page">
    <h2>推荐</h2>
    <RecommendationList :destinations="recommendedDestinations" />
    
    <!-- 居中放置的搜索框和按钮 -->
    <div class="search-container">
      <SearchBar @search="performSearch" />
    </div>

    <SearchResults :results="searchResults" />

    <!-- 登录组件 -->
    <Login v-if="!isLoggedIn && show" @close="close" />

    <Navbar />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import RecommendationList from './RecommendationList.vue';
import SearchBar from './SearchBar.vue';
import SearchResults from './SearchResults.vue';
import Navbar from './Navbar.vue';
import Login from './Login.vue';

const recommendedDestinations = ref([]);
const searchResults = ref([]);
const isLoggedIn = ref(false); // 用户登录状态

const performSearch = async (query) => {
  try {
    const [attractionsResponse, facilitiesResponse, diariesResponse] = await Promise.all([
      axios.get('http://localhost:8000/api/search/attractions/', { params: { name: query } }),
      axios.get('http://localhost:8000/api/search/facilities/', { params: { locationId: 123, type: 'restaurant', radius: 500 } }),
      axios.get('http://localhost:8000/api/search/diaries/', { params: { keywords: query } })
    ]);

    searchResults.value = [
      ...attractionsResponse.data.attractions,
      ...facilitiesResponse.data.facilities,
      ...diariesResponse.data.diaries
    ];
  } catch (error) {
    console.error('搜索失败:', error);
    // 在此处添加用户反馈，如错误提示
  }
};

const show = ref(false); // 初始状态为隐藏登录界面

const openLogin = () => {
  show.value = true; // 控制显示登录界面
};

const close = () => {
  show.value = false; // 控制隐藏登录界面
};

// 监听用户登录状态的变化，如果用户登录成功，则隐藏登录组件
watch(isLoggedIn, (newValue) => {
  if (newValue) {
    close(); // 登录成功后关闭登录组件
  }
});

// 在进入主页后一段时间后显示登录组件
setTimeout(() => {
  openLogin();
}, 5000); // 5秒后显示登录组件
</script>

<style scoped>
.home-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

/* 居中放置的搜索框和按钮 */
.search-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px; /* 添加间距 */
}
</style>
