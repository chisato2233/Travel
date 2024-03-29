<!-- 寻路页面，到单个目的地，多个目的地 -->
<!-- 在页面最底下还有一个导航栏 -->

<template>
    <div class="travel-container">
      <h2>寻路</h2>
      <div class="form-group">
        <label for="startLocation">起点：</label>
        <input type="text" id="startLocation" v-model="startLocation" placeholder="请输入起点">
      </div>
      <div class="form-group">
        <label for="endLocation">终点：</label>
        <input type="text" id="endLocation" v-model="endLocation" placeholder="请输入终点">
      </div>
      <button class="search-button" @click="searchRoute">查询</button>
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
  
  const searchRoute = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/routes/optimal', {
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
    }
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
  
  input {
    width: 100%;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  .search-button {
    width: 100%;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
    background-color: #007bff;
    color: #fff;
  }
  
  .search-button:hover {
    background-color: #0056b3;
  }
  
  .error-message {
    color: red;
    text-align: center;
    margin-top: 10px;
  }
  </style>   
  