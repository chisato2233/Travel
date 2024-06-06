<template>
    <div class="all-locations">
      <h2>全部景点</h2>
      <ul class="location-list">
        <li v-for="(location, index) in locations" :key="index" class="location-item">{{ location }}</li>
      </ul>
    </div>
  
    <!-- 导航栏组件 -->
    <Navbar />
  </template>
  
  <script setup>
  import Navbar from './Navbar.vue'; // 导入导航栏组件
  import { validLocations } from './locations'; // 导入景点数据
  
  const locations = validLocations;
  </script>
  
  <style scoped>
  .all-locations {
    width: 800px;
    margin: auto;
    text-align: center;
    color: #333;
  }
  
  h2 {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
  }
  
  .location-list {
    list-style-type: none;
    padding: 0;
  }
  
  .location-item {
    margin-bottom: 5px;
    padding: 8px 20px;
    background-color: #4CAF50;
    border-radius: 20px;
    display: inline-block;
    font-size: 16px;
    font-weight: bold;
    color: #fff;
  }
  </style>
  