<template>
  <div>
    <!-- 模糊背景 -->
    <div class="blur-background" v-show="showLogin || showRegister"></div>
    <!-- 中心盒子容器 -->
    <transition name="slide">
      <div class="center-screen" v-show="showLogin || showRegister">
        <div class="center-box">
          <button class="close-button" @click="closeLogin">✕</button>
          <div class="tab-buttons">
            <button :class="{ active: showLogin }" @click="showLogin = true; showRegister = false" :disabled="isProcessing">登录</button>
            <button :class="{ active: showRegister }" @click="showLogin = false; showRegister = true" :disabled="isProcessing">注册</button>
          </div>
          <!-- 登录表单 -->
          <form v-if="showLogin" @submit.prevent="login">
            <div class="form-group">
              <input type="text" id="username" v-model="username" placeholder="用户名">
            </div>
            <div class="form-group">
              <input type="password" id="password" v-model="password" placeholder="密码">
            </div>
            <div class="button-group">
              <button type="submit" class="login-button" :class="{ disabled: isProcessing }" :disabled="isProcessing">登录</button>
            </div>
          </form>
          <!-- 注册表单 -->
          <form v-if="showRegister" @submit.prevent="register">
            <div class="form-group">
              <input type="text" id="username" v-model="username" placeholder="用户名">
            </div>
            <div class="form-group">
              <input type="email" id="email" v-model="email" placeholder="邮箱">
            </div>
            <div class="form-group">
              <input type="password" id="password" v-model="password" placeholder="密码">
            </div>
            <div class="button-group">
              <button type="submit" class="register-button" :class="{ disabled: isProcessing }" :disabled="isProcessing">注册</button>
            </div>
          </form>
          <!-- 错误消息提示 -->
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const isProcessing = ref(false); // 正在处理中

const showLogin = ref(true); // 控制登录界面显示与隐藏的状态
const showRegister = ref(false); // 控制注册界面显示与隐藏的状态

const login = async () => {
  try {
    errorMessage.value = '';
    isProcessing.value = true;
    const response = await axios.post('http://localhost:8000/api/users/login/', {
      username: username.value,
      password: password.value
    });
    const data = response.data;
    const token = response.data.token;
    localStorage.setItem('token', token);
    console.log('登录成功:', data);
    await isLoggedIn(); // 更新用户登录状态
    router.push({ name: 'ProfilePage' });
  } catch (error) {
    console.error('登录失败:', error);
    errorMessage.value = '登录失败，请检查用户名和密码是否正确。';
  } finally {
    isProcessing.value = false;
  }
};

const register = async () => {
  try {
    errorMessage.value = '';
    isProcessing.value = true;
    const response = await axios.post('http://localhost:8000/api/users/register/', {
      username: username.value,
      email: email.value,
      password: password.value
    });
    const data = response.data;
    console.log('注册成功:', data);
    await isLoggedIn(); // 更新用户登录状态
    // 注册成功后的逻辑，例如提示用户、跳转页面等
  } catch (error) {
    console.error('注册失败:', error);
    errorMessage.value = '注册失败，请稍后重试。';
  } finally {
    isProcessing.value = false;
  }
};

const closeLogin = () => {
  showLogin.value = false;
  showRegister.value = false;
  router.push({ name: 'HomePage' });
};

async function isLoggedIn() {
  try {
    const response = await axios.get('http://localhost:8000/api/users/user/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    });
    if (response.status === 200) {
      console.log('用户已登录');
      return true;
    }
  } catch (error) {
    console.error('用户未登录:', error);
    return false;
  }
}
</script>


<style scoped>
/* 模糊背景样式 */
.blur-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3); /* 调浅一点的背景色 */
  backdrop-filter: blur(10px); /* 添加模糊效果，也可以调整模糊程度 */
  z-index: 999; /* 确保模糊背景位于其他内容之下 */
}

/* 确保整个屏幕都被覆盖，并设置中心定位 */
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000; /* 提高 z-index 以确保在模糊背景之上 */
}

/* 中心盒子的样式 */
.center-box {
  padding: 40px; /* 调大一点 */
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  width: 350px; /* 调大一点 */
  position: relative; /* 为了定位关闭按钮 */
  z-index: 1001; /* 确保位于 center-screen 和模糊背景之上 */
}

/* 关闭按钮样式 */
.close-button {
  position: absolute;
  top: -20px;
  right: -20px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background-color: #ff4d4d;
  color: white;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.close-button:hover {
  background-color: #e60000;
}

.close-button:active {
  background-color: #cc0000;
}

.form-group {
  margin-bottom: 30px; /* 增大表单项之间的垂直间距 */
}

/* 登录和注册按钮样式 */
.login-button,
.register-button {
  width: 100%; /* 设置按钮宽度为父容器宽度 */
  margin-top: 10px;
  color: white; /* 设置字体颜色为白色 */
  font-weight: bold; /* 设置字体加粗 */
  background-color: #4CAF50; /* 设置按钮初始颜色 */
  border: none;
  padding: 10px;
  border-radius: 20px; /* 将按钮形状修改为两端是圆形 */
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-button:hover,
.register-button:hover {
  background-color: #308834; /* 设置鼠标悬停时的颜色变深 */
}

.login-button:active,
.register-button:active {
  background-color: #09803c; /* 设置鼠标悬停时的颜色变深 */
}

/* 添加禁用状态下的按钮样式 */
.tab-buttons button.disabled {
  background-color: #ccc; /* 禁用时按钮颜色 */
  cursor: not-allowed; /* 设置禁用时的鼠标样式 */
}

.tab-buttons button.disabled:hover {
  background-color: #ccc; /* 禁用时按钮悬停颜色 */
}

.login-button.disabled,
.register-button.disabled {
  background-color: #ccc; /* 禁用时按钮颜色 */
  cursor: not-allowed; /* 设置禁用时的鼠标样式 */
}

.login-button.disabled:hover,
.register-button.disabled:hover {
  background-color: #ccc; /* 禁用时按钮悬停颜色 */
}

/* 输入框样式 */
input[type="text"],
input[type="password"],
input[type="email"] {
  width: 100%; /* 设置输入框宽度 */
  padding: 12px; /* 增加输入框的内边距 */
  border: 1px solid #ccc;
  border-radius: 20px; /* 将输入框的两端修改为圆形 */
  box-sizing: border-box; /* 确保填充和边框包含在元素的总宽度和高度内 */
  height: 40px; /* 增加输入框的高度 */
}

/* 输入框在聚焦时的样式 */
input[type="text"]:focus,
input[type="password"]:focus,
input[type="email"]:focus {
  outline: none; /* 去掉默认的聚焦边框 */
  border-color: #4CAF50; /* 聚焦时边框颜色 */
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.5); /* 聚焦时的阴影效果 */
}


h2 {
  text-align: center;
  color: #333;
}

/* 过渡动画 */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.5s ease; /* 设置过渡效果 */
}
.slide-enter, .slide-leave-to /* .slide-leave-active 在版本 2.1.8 及以上版本中生效 */ {
  transform: translateY(100%); /* 初始位置 */
}
.slide-leave-active {
  transform: translateY(100%); /* 收回到底部 */
}

/* 选项卡按钮样式 */
.tab-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 50px;
}

.tab-buttons button {
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 20px; /* 将按钮形状修改为两端是圆形 */
  cursor: pointer;
  background-color: #4CAF50; /* 设置按钮初始颜色为绿色 */
  color: white; /* 设置字体颜色为白色 */
  font-weight: bold; /* 设置字体加粗 */
  
  transition: background-color 0.3s;
}

.tab-buttons button.active {
  background-color: #09803c; /* 设置选中按钮的颜色为深绿色 */
}

.tab-buttons button:hover {
  background-color: #308834; /* 设置鼠标悬停时的颜色变深 */
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}

</style>
