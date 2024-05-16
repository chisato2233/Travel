<template>
  <div class="profile-page">
    <h2>个人主页</h2>
    
    <!-- 显示错误信息 -->
    <p v-if="error" class="error-message">{{ error }}</p>
    
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
    <Navbar />
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';

const userInfo = ref(null);
const newEmail = ref('');
const error = ref(null);

const isUserLoggedIn = ref(false);

onMounted(async () => {
  await fetchUserInfo();
});

const fetchUserInfo = async () => {
  try {
    const token = getToken();
    if (token) {
      isUserLoggedIn.value = await isLoggedIn();
      const response = await axios.get('http://localhost:8000/api/users/user/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userInfo.value = response.data;
    }
  } catch (error) {
    console.error('获取用户信息失败:', error);
    showError('获取用户信息失败: ' + error.message);
  }
};

const updateUserInfo = async () => {
  try {
    const token = getToken();
    if (token) {
      const response = await axios.put('http://localhost:8000/api/users/update/', { email: newEmail.value }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log(response.data.message);
      await fetchUserInfo();
      newEmail.value = '';
    }
  } catch (error) {
    console.error('更新用户信息失败:', error);
    showError('更新用户信息失败: ' + error.message);
  }
};

const logout = async () => {
  try {
    const token = getToken();
    if (token) {
      const response = await axios.post('http://localhost:8000/api/users/logout/', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log(response.data.message);
      isUserLoggedIn.value = false;
      window.location.href = '/login';
    }
  } catch (error) {
    console.error('注销失败:', error);
    showError('注销失败: ' + error.message);
  }
};

const showError = (errorMessage) => {
  error.value = errorMessage;
};

function getToken() {
  return localStorage.getItem('token');
}

async function isLoggedIn() {
  try {
    const response = await axios.get('http://localhost:8000/api/users/check-auth', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    return response.data.isLoggedIn;
  } catch (error) {
    console.error('检查用户登录状态失败:', error);
    return false;
  }
}
</script>

<style scoped>

.error-message {
  color: red;
}

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
