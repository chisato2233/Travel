<!-- 这是主页，展示推荐界面，搜索栏 -->
                      <!-- 搜索栏：景点查询，设施与美食查询 -->
<!-- 在页面最底下还有一个导航栏 -->

<template>
  <div class="home-page">
    <h2>推荐</h2>
    <div class="recommendation">
      <!-- 推荐目的地列表 -->
      <div v-for="destination in recommendedDestinations" :key="destination.id" class="destination-card">
        <img :src="destination.imageURL" alt="Destination Image" class="destination-image">
        <div class="destination-info">
          <h3>{{ destination.name }}</h3>
          <p>{{ destination.description }}</p>
          <div class="destination-meta">
            <span class="rating">评分: {{ destination.rating }}</span>
            <span class="popularity">人气: {{ destination.popularity }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <input type="text" v-model="searchQuery" placeholder="搜索">
      <button @click="search">搜索</button>
    </div>

    <!-- 显示搜索结果 -->
    <div class="search-results" v-if="searchResults.length > 0">
      <h3>搜索结果</h3>
      <div v-for="result in searchResults" :key="result.id" class="search-result">
        <h4>{{ result.title }}</h4>
        <p>{{ result.summary }}</p>
        <p v-if="result.type">类型: {{ result.type }}</p>
        <p v-if="result.rating">评分: {{ result.rating }}</p>
        <p v-if="result.popularity">人气: {{ result.popularity }}</p>
        <p v-if="result.distance">距离: {{ result.distance }} 米</p>
        <p>{{ result.date }}</p>
        <p>作者: {{ result.username }}</p>
      </div>
    </div>

    <!-- 导航栏 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件

const recommendedDestinations = ref([]);
const searchQuery = ref('');
const searchResults = ref([]);

const search = async () => {
  try {
    // 搜索景点
    const attractionsResponse = await axios.get('http://localhost:8000/api/search/attractions', {
      params: {
        name: searchQuery.value // 使用搜索查询作为景点名称
      }
    });
    recommendedDestinations.value = attractionsResponse.data.attractions;

    // 搜索附近设施与美食
    const facilitiesResponse = await axios.get('http://localhost:8000/api/search/facilities', {
      params: {
        locationId: 123, // 例如，假设用户当前位置的唯一标识符为123
        type: 'restaurant', // 设施类型为餐厅
        radius: 500 // 搜索半径为500米
      }
    });
    searchResults.value = facilitiesResponse.data.facilities;

    // 搜索日记
    const diariesResponse = await axios.get('http://localhost:8000/api/search/diaries', {
      params: {
        keywords: searchQuery.value // 使用搜索查询作为关键词
      }
    });
    searchResults.value = searchResults.value.concat(diariesResponse.data.diaries);
  } catch (error) {
    console.error('搜索失败:', error);
  }
};
</script>

<style scoped>
.home-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.recommendation {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.destination-card {
  width: calc(50% - 10px);
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow: hidden;
}

.destination-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.destination-info {
  padding: 10px;
}

.destination-meta {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.search-bar {
  margin-top: 20px;
}

input[type="text"] {
  padding: 8px;
  width: 200px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #007bff;
  color: #fff;
}

button:hover {
  background-color: #0056b3;
}

.search-results {
  margin-top: 20px;
}

.search-result {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.search-result h4 {
  margin-bottom: 5px;
}

.search-result p {
  margin: 5px 0;
}
</style>