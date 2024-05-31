<template>
    <div class="not-found">
      <h1>页面未找到</h1>
      <p>您要查找的页面不存在。</p>
      <router-link to="/">返回主页</router-link>
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  onMounted(() => {
    setTimeout(() => {
      router.push({ name: 'HomePage' });
    }, 5000); // 5秒后导航到首页
  });
  </script>
  
  <style scoped>
  .not-found {
    text-align: center;
    margin-top: 50px;
  }
  
  .not-found h1 {
    font-size: 2em;
    color: #ff4d4f;
  }
  
  .not-found p {
    margin-top: 20px;
  }
  
  .not-found a {
    margin-top: 20px;
    display: inline-block;
    color: #12b741;
    text-decoration: underline;
  }
  </style>
  