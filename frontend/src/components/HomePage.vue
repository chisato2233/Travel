<template>
  <div class="home-page">
    <RecommendationList :destinations="recommendedDestinations" />

    <!-- 居中放置的搜索框和按钮 -->
    <div class="search-container">
      <SearchBar @search="performSearch" @updateSearchType="updateSearchType"
        @updateSearchParams="updateSearchParams" />
    </div>

    <SearchResults :results="searchResults" />

    <!-- 登录组件 -->
    <Login v-if="!isLoggedIn && showLogin" @close="handleLoginClose" />

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

// 从 localStorage 中获取令牌，如果不存在则返回 null
const token = localStorage.getItem('token');

const searchType = ref('attractions'); // 初始搜索类型
const searchParams = ref({}); // 搜索参数

const performSearch = async (query) => {
  try {
    let response;
    if (searchType.value === 'attractions') {
      response = await axios.get('http://localhost:8000/api/search/attractions/', { params: { ...searchParams.value, name: query } });
      searchResults.value = response.data.attractions;
    } else if (searchType.value === 'facilities') {
      response = await axios.get('http://localhost:8000/api/search/facilities/', { params: { ...searchParams.value } });
      searchResults.value = response.data.facilities;
    } else if (searchType.value === 'diaries') {
      response = await axios.get('http://localhost:8000/api/search/diaries/', { params: { ...searchParams.value, keywords: query } });
      searchResults.value = response.data.diaries;
    }
  } catch (error) {
    console.error('搜索失败:', error);
    // 在此处添加用户反馈，如错误提示
  }
};

// 判断用户是否已经登录，如果已经登录且令牌有效，则不再显示登录界面
const isLoggedIn = ref(!!token);

const showLogin = ref(false); // 初始状态为隐藏登录界面
const manualLoginClose = ref(false); // 标志位，用于跟踪用户是否手动关闭了登录界面

const openLogin = () => {
  if (!manualLoginClose.value) { // 仅在用户未手动关闭登录界面的情况下自动显示
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
setTimeout(() => {
  openLogin();
}, 5000); // 5秒后显示登录组件

const updateSearchType = (type) => {
  searchType.value = type;
};

const updateSearchParams = (params) => {
  searchParams.value = params;
};
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
  margin-bottom: 20px;
  /* 添加间距 */
}
</style>