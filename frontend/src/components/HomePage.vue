<template>
  <div class="home-page">
    <!-- 居中放置的搜索框和按钮 -->
    <div class="search-container">
      <SearchBar @search="performSearch" @updateSearchType="updateSearchType" @updateSearchParams="updateSearchParams" />
    </div>

    <SearchResults :results="searchResults" :selectedType="searchType" />

    <!-- 登录组件 -->
    <Login v-if="!isLoggedIn && showLogin" @close="handleLoginClose" />

    <!-- 显示搜索失败消息 -->
    <p v-if="searchError" class="error-message">{{ searchError }}</p>

    <Navbar />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import SearchBar from './SearchBar.vue';
import SearchResults from './SearchResults.vue';
import Navbar from './Navbar.vue';
import Login from './Login.vue';

const router = useRouter();

const recommendedDestinations = ref([]);
const searchResults = ref([]);

// 从 localStorage 中获取令牌，如果不存在则返回 null
const token = localStorage.getItem('token');

const searchType = ref('attractions'); // 初始搜索类型
const searchParams = ref({}); // 搜索参数
const searchError = ref(''); // 搜索失败消息

const performSearch = async (query) => {
  try {
    let response;
    if (searchType.value === 'attractions') {
      response = await axios.get('http://localhost:8000/api/search/attractions', {
        headers: {
          'Authorization': `Bearer ${token}`
        }, params: { ...searchParams.value, name: query } });
      searchResults.value = response.data.attractions;
    } else if (searchType.value === 'facilities') {
      response = await axios.get('http://localhost:8000/api/search/facilities/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }, params: { ...searchParams.value } });
      searchResults.value = response.data.facilities;
    } else if (searchType.value === 'diaries') {
      response = await axios.get('http://localhost:8000/api/search/diaries/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }, params: { ...searchParams.value, keywords: query } });
      searchResults.value = response.data.diaries;
    }
    // 搜索成功时清除搜索失败消息
    searchError.value = '';
  } catch (error) {
    console.error('搜索失败:', error);
    if (error.response && error.response.status === 404) {
      router.push({ name: 'NotFound' });
    } else {
      // 显示搜索失败消息
      searchError.value = '搜索失败，请稍后重试。';
    }
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

.error-message {
  color: #ff4d4f; /* 红色用于错误消息 */
  margin-top: 10px; /* 添加一些顶部间距 */
  text-align: center;
}
</style>
