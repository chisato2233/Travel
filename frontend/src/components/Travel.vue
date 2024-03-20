<template>
    <div class="travel-container">
      <h2>旅行页面</h2>
      <!-- 在这里添加旅行页面的内容 -->
      <router-link to="/diary" class="diary-link">游学日记</router-link>
    </div>
  </template>
  
  <script setup>
  // 在这里添加相关逻辑代码
  </script>
  
  <style scoped>
  .travel-container {
    text-align: center;
  }
  
  .diary-link {
    margin-top: 20px;
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #007bff;
    border-radius: 5px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
  }
  
  .diary-link:hover {
    background-color: #0056b3;
  }
  </style>
  