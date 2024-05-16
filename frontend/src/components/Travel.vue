<template>
  <div class="travel-container">
    <h2>寻路</h2>
    <div class="form-group">
      <input type="text" id="startLocation" v-model="startLocation" placeholder="起点" class="rounded-input" @focus="inputFocus">
    </div>
    <div class="form-group">
      <input type="text" id="endLocation" v-model="endLocation" placeholder="终点" class="rounded-input" @focus="inputFocus">
    </div>
    <button class="search-button" @click="searchRoute" :disabled="isSearching">
      <span v-if="isSearching">查询中...</span>
      <span v-else>查询</span>
    </button>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
  
  <!-- 导航栏组件 -->
  <Navbar />
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件

const startLocation = ref('');
const endLocation = ref('');
const errorMessage = ref('');
const isSearching = ref(false); // 控制查询状态

const searchRoute = async () => {
  try {
    isSearching.value = true; // 开始查询，禁用按钮
    const response = await axios.post('http://localhost:8000/api/routes/optimal/', {
      startLocation: startLocation.value,
      endLocation: endLocation.value,
      strategy: 'shortest' // 默认选择最短路线策略
    });
    const data = response.data;
    console.log('最优路线:', data);
    // 在这里处理获取最优路线成功后的逻辑，例如显示路线信息等
  } catch (error) {
    console.error('查询失败:', error);
    if (error.response && error.response.status === 400) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = '查询失败，请稍后重试。';
    }
  } finally {
    isSearching.value = false; // 查询结束，启用按钮
  }
};

const inputFocus = () => {
  errorMessage.value = ''; // 清除错误消息
};
</script>

<style scoped>
.travel-container {
  width: 400px;
  margin: auto;
}

h2 {
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.rounded-input {
  width: 100%;
  padding: 8px;
  border-radius: 20px; /* 两端圆形 */
  border: 1px solid #ccc;
}

.rounded-input:focus {
  border-color: #4CAF50; /* 输入框聚焦时边框颜色变成绿色 */
}

.search-button {
  width: 100%;
  padding: 8px 16px;
  border: none;
  border-radius: 20px; /* 两端圆形 */
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #4CAF50; /* 绿色主色 */
  color: #fff;
}

.search-button[disabled] {
  background-color: #ccc; /* 禁用状态下按钮颜色变成灰色 */
  cursor: not-allowed; /* 设置鼠标样式为禁用 */
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
