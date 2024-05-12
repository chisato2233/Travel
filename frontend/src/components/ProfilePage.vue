<!-- 未登陆时，跳转到登录界面（Login.vue），若无账号，可在登陆界面中选择注册（Register.vue）
     已登录，自动显示个人信息，通过按钮更新用户信息，用户注销 
            自动显示个人信息，通过按钮更新用户信息，用户注销的功能由UserInfoForm.vue实现 -->

<!-- 在页面最底下还有一个导航栏 -->
<template>
  <div class="profile-page">
    <h2>个人主页</h2>
    <!-- 显示用户信息 -->
    <div v-if="userInfo">
      <p><strong>用户名:</strong> {{ userInfo.username }}</p>
      <p><strong>Email:</strong> {{ userInfo.email }}</p>
    </div>
    <p v-else>加载中...</p>

    <!-- 更新用户信息表单 -->
    <form @submit.prevent="updateUserInfo" v-if="userInfo">
      <h3>更新用户信息</h3>
      <label for="email">新Email:</label>
      <input type="email" id="email" v-model="newEmail" required>
      <button type="submit">更新</button>
    </form>

    <!-- 注销按钮 -->
    <button @click="logout" v-if="userInfo">注销</button>

    <!-- 导航栏组件 -->
    <Navbar/>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue'; // 导入导航栏组件

const userInfo = ref(null);
const newEmail = ref('');

// 页面加载时获取用户信息
onMounted(async () => {
  await fetchUserInfo();
});

// 获取用户信息的方法
const fetchUserInfo = async () => {
  try {
    console.log(`Bearer ${getToken()}`);

    const response = await axios.get('http://localhost:8000/api/users/user/', {
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
    userInfo.value = response.data;
  } catch (error) {
    console.error('获取用户信息失败:', error);
    // 处理错误，例如重定向到登录页面
  }
};

// 更新用户信息的方法
const updateUserInfo = async () => {
  try {
    const response = await axios.put('http://localhost:8000/api/users/update', { email: newEmail.value }, {
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
    console.log(response.data.message); // 打印成功更新用户信息的消息
    await fetchUserInfo(); // 更新用户信息后刷新页面显示最新信息
    newEmail.value = ''; // 清空输入框
  } catch (error) {
    console.error('更新用户信息失败:', error);
    // 处理错误，例如显示错误消息
  }
};

// 注销方法
const logout = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/users/logout', {}, {
      headers: {
        Authorization: `Bearer ${getToken()}`
      }
    });
    console.log(response.data.message); // 打印成功注销的消息
    // 导航到登录页面
    window.location.href = '/login';
  } catch (error) {
    console.error('注销失败:', error);
    // 处理错误，例如显示错误消息
  }
};

// 获取存储在本地的用户token
function getToken() {
  return localStorage.getItem('token');
}
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

form {
  margin-top: 20px;
}

input {
  margin-bottom: 10px;
}

button {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>


    