<!-- 注册成功后，通过返回按钮，回跳到登陆界面，进行登录 -->
<!-- 在页面最底下还有一个导航栏 -->

<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <!-- <label for="username">用户名：</label> -->
        <input type="text" id="username" v-model="username" placeholder="用户名">
      </div>
      <div class="form-group">
        <!-- <label for="email">邮箱：</label> -->
        <input type="email" id="email" v-model="email" placeholder="邮箱">
      </div>
      <div class="form-group">
        <!-- <label for="password">密码：</label> -->
        <input type="password" id="password" v-model="password" placeholder="密码">
      </div>
      <div class="button-group">
        <button type="submit" class="register-button">注册</button>
        <button type="button" class="back-button" @click="goToLogin">返回</button> <!-- Added back button -->
      </div>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </div>
  <!-- Insert Navbar component below -->
  <Navbar />
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // Import useRouter
import Navbar from './Navbar.vue'; // Import Navbar component

const username = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter(); // Define useRouter

const register = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/users/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    });
    const data = response.data;
    console.log('注册成功:', data);
    // 在这里处理注册成功后的逻辑，例如提示用户、跳转页面等
  } catch (error) {
    console.error('注册失败:', error);
    if (error.response && error.response.status === 400) {
      errorMessage.value = error.response.data.error;
    } else {
      errorMessage.value = '注册失败，请稍后重试。';
    }
  }
};

const goToLogin = () => {
  router.push({ name: 'Login' }); // Redirect to Login.vue on click of back button
};
</script>

<style scoped>
.register-container {
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

.button-group {
  text-align: center;
}

.register-button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #007bff;
  color: #fff;
}

.register-button:hover {
  background-color: #0056b3;
}

.back-button {
  margin-left: 10px; /* Added margin to separate buttons */
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  background-color: #ccc;
  color: #000;
}

.back-button:hover {
  background-color: #999;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>


  