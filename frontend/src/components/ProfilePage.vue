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
      isUserLoggedIn.value = true;
      const response = await axios.get('http://localhost:8000/api/auth/user/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      userInfo.value = response.data;
    }
  } catch (error) {
    console.error('获取用户信息失败:', error);
    if (error.response && error.response.status === 401) {
      showError('Token无效或已过期');
    } else {
      showError('获取用户信息失败: ' + error.message);
    }
  }
};

const updateUserInfo = async () => {
  try {
    const token = getToken();
    if (token) {
      const response = await axios.put('http://localhost:8000/api/auth/update/', { email: newEmail.value }, {
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
    if (error.response && (error.response.status === 400 || error.response.status === 401)) {
      showError('请求无效或未经授权');
    } else {
      showError('更新用户信息失败: ' + error.message);
    }
  }
};

const logout = async () => {
  try {
    const token = getToken();
    const refreshToken = getRefreshToken();
    if (token && refreshToken) {
      const response = await axios.post('http://localhost:8000/api/auth/logout/', { refreshToken: refreshToken }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      console.log(response.data.message);
      localStorage.removeItem('token');  // 清除 token
      localStorage.removeItem('refreshToken');  // 清除 refresh token
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

function getRefreshToken() {
  return localStorage.getItem('refreshToken');
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
  background-color: #28a745; /* 绿色背景 */
  color: white; /* 白色字体 */
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold; /* 加粗字体 */
}

button:hover {
  background-color: #218838; /* 深绿色背景 */
}
</style>
