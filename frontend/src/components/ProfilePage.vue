<template>
  <div class="profile-page">
    <h2>个人主页</h2>

    <!-- 显示错误信息 -->
    <p v-if="error" class="error-message">{{ error }}</p>

    <!-- 显示用户信息 -->
    <div v-if="userInfo" class="user-info">
      <p><strong>用户名:</strong> {{ userInfo.username }}</p>
      <p><strong>Email:</strong> {{ userInfo.email }}</p>
    </div>
    <p v-else>加载中...</p>

    <!-- 更新用户信息表单 -->
    <form @submit.prevent="updateUserInfo" v-if="userInfo" class="update-form">
      <h3>更新用户信息</h3>
      <label for="email">新Email:</label>
      <input type="email" id="email" v-model="newEmail" required>
      <button type="submit">更新</button>
    </form>

    <!-- 注销按钮 -->
    <button @click="logout" v-if="userInfo" class="logout-button">注销</button>

    <!-- 包含 Diary 组件 -->
    <Diary />

    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';
import Diary from './Diary.vue'; // 导入 Diary 组件
// 导入路由实例
import router from '../router/index';

const userInfo = ref(null);
const newEmail = ref('');
const error = ref(null);

const isUserLoggedIn = ref(false);
const showErrorAndRedirectToLogin = (errorMessage) => {
  error.value = errorMessage;
  if (errorMessage === 'Token无效或已过期') {
    // 使用编程式导航将用户导航到Login.vue界面
    router.push({ name: 'Login' });
  }
};

onMounted(async () => {
  await fetchUserInfo();
});

const fetchUserInfo = async () => {
  try {
    const token = getToken();
    if (token) {
      isUserLoggedIn.value = true;
      const response = await axios.get('http://localhost:8000/api/users/user/', {
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
      showErrorAndRedirectToLogin('Token无效或已过期');
      router.push('Login/');
    } else {
      showError('获取用户信息失败: ' + error.message);
    }
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
      const response = await axios.post('http://localhost:8000/api/users/logout/', { refreshToken: refreshToken }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (response.status === 200) {
        console.log(response.data.message);
        localStorage.removeItem('token');  // 清除 token
        localStorage.removeItem('refreshToken');  // 清除 refresh token
        isUserLoggedIn.value = false;
        router.push('/login'); // 跳转到登陆界面
      } else {
        showError('注销失败: ' + response.data.error);
      }
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
  color: #ff4d4f; /* Red color for error messages */
}

.profile-page {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-info {
  background-color: #f0f2f5; /* Light gray background for user information */
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.update-form {
  margin-top: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #d9d9d9; /* Light gray border */
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 8px 16px;
  background-color: #4fea51; /* Blue color for buttons */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease; /* Smooth transition on hover */
}

.logout-button{
  width: 250px;
  padding: 8px 16px;
  background-color: #4fea51; /* Blue color for buttons */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease; /* Smooth transition on hover */
}

button:hover, .logout-button:hover {
  background-color: #22bd07; /* Darker blue color on hover */
}

.logout-button {
  margin-top: 10px;
  background-color: #4fdd60; /* Red color for logout button */
}

</style>
