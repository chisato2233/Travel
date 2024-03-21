<template>
  <div class="login-container">
    <div class="login-form">
      <h2>用户登录</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="username">用户名：</label>
          <input type="text" id="username" v-model="username" placeholder="请输入用户名">
        </div>
        <div class="form-group">
          <label for="password">密码：</label>
          <input type="password" id="password" v-model="password" placeholder="请输入密码">
        </div>
        <div class="button-group">
          <button type="submit" class="login-button">登录</button>
        </div>
      </form>
    </div>
    <div class="forgot-password">
      <button type="button" class="forgot-password-button" @click="forgotPassword">找回密码</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // Import useRouter

// Define useRouter
const router = useRouter();

// 定义响应式变量
const username = ref('');
const password = ref('');

// 登录函数
const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/users/login/', {
      username: username.value,
      password: password.value
    });
    const data = response.data;
    console.log('登录成功:', data);
    // 在这里处理登录成功后的逻辑，例如保存token、跳转页面等
    router.push({ name: 'Travel' }); // Redirect to Travel.vue on successful login
  } catch (error) {
    console.error('登录失败:', error);
    // 在这里处理登录失败后的逻辑，例如提示用户、清除输入等
  }
};

// 找回密码函数
const forgotPassword = () => {
  // 在此处添加找回密码的逻辑，例如跳转到找回密码页面或者发送重置密码邮件等
  console.log('点击了找回密码按钮');
};
</script>

<style scoped>
.login-container {
  position: absolute;
  right: 50px; /* 向右移动距离右边的页面边界有50个像素 */
  width: 500px; /* 宽度400px */
  height: 400px; /* 高度400px */
  margin: auto; /* 水平居中 */
  top: 0; /* 顶部对齐 */
  bottom: 0; /* 底部对齐 */
  border: 1px solid #ccc; /* 灰色边框 */
  border-radius: 5px;
  background-color: #fff; /* 白色背景 */
}

.login-form {
  text-align: center; /* 居中 */
}

.login-form h2 {
  font-size: 24px; /* 调整字体大小 */
}

.form-group {
  margin-bottom: 30px; /* 增大垂直距离 */
}

input {
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.button-group {
  margin-top: 10px;
}

.login-button {
  padding: 8px; /* 调整按钮大小 */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  width: calc(50% - 5px); /* 将按钮宽度设置为父容器的一半 */
  background-color: #007bff; /* 蓝色 */
  color: #fff;
}

.login-button:hover {
  background-color: #0056b3; /* 鼠标悬停时的背景色 */
}

.forgot-password {
  margin-top: 20px; /* 调整找回密码按钮与登录按钮的距离 */
  text-align: center; /* 文字居中 */
}

.forgot-password-button {
  padding: 8px; /* 调整按钮大小 */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  width: calc(25% - 5px); /* 将按钮宽度设置为父容器的1/4 */
  background-color: #ccc; /* 灰色 */
  color: #000;
}

.forgot-password-button:hover {
  background-color: #999; /* 鼠标悬停时的背景色 */
}
</style>

















