<template>
  <div id="app">
    <Header />
    <div class="content">
      <img src="./assets/登陆界面图片1.jpg" alt="Left Image" class="left-image">
      <Login />
    </div>
  </div>
</template>

<script setup>
import Login from './components/Login.vue';
import Header from './components/Header.vue';
</script>

<style>
#app {
  display: flex;
  flex-direction: column; /* 垂直方向排列子元素 */
  align-items: center; /* 子元素水平居中对齐 */
  height: 100vh; /* 占满整个视口高度 */
  background: linear-gradient(to bottom right, #f0e68c, #98fb98); /* 渐变的浅黄绿色背景 */
}

.content {
  width: 100%; /* 内容宽度 */
  display: flex;
}

.left-image {
  width: 50%; /* 图片宽度占据左半部分 */
  height: auto; /* 自适应高度 */
  margin-top: 80px; /* 距离顶部80像素 */
  margin-left: 50px; /* 距离整个页面左边界20像素 */
}
</style>







