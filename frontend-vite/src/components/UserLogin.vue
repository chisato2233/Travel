<template>
  <div class="app-container">
    <div class="login-container">
      <h2>登录</h2>
        <vs-input class="inputx" placeholder="用户名" id="username" v-model="credentials.username" required />
        <vs-input class="inputx" placeholder="密码" id="password" v-model="credentials.password" required />
        <vs-button type="gradient" @click="login">登录</vs-button>
      
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    async login() {
      
      try {
        const response = await axios.post('/api/users/login/', this.credentials);
        console.log('Login successful', response.data);
        // 保存token和用户信息，可以保存到localStorage或Vuex
        localStorage.setItem('token', response.data.token);
        this.$router.push({ name: 'Home' }); // 假设登录成功后跳转到主页
      } catch (error) {
        console.error('Login failed', error.response.data);
        this.$vs.notify({
          title: '登陆失败😭😭😭😭',
          text: '用户名或密码错误',
          color:'danger'
        })
      }
    }
  }
}
</script>

<style scoped>a
html, body {
  margin: 0;
  padding: 0;
  color: red;
}

.app-container {
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #FFB6C1 0%, #A9C9FF 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 使用视窗高度确保整个页面充满整个屏幕 */

}

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 400px; /* 使用固定宽度以保持在不同屏幕上的一致性 */
  padding: 50px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  border-radius: 15px;
  background: #ffffff; /* 添加轻微的背景色提高可读性 */
}

h2, .inputx, .vs-button {
  color: #34568B; /* 深蓝色 */
}

.inputx, .vs-button {
  width: 100%; /* 确保输入框和按钮宽度一致 */
  margin-bottom: 20px; /* 保持元素之间的间隔 */
}
.vs-button {
  background-color: #FFB6C1; /* 粉红色按钮背景 */
  border: none;
  color: white; /* 白色文本提高对比度 */
}
.inputx, .vs-button {
  border-radius: 4px; /* 圆角 */
  box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* 轻微阴影增加立体感 */
}

h2 {
  margin-bottom: 30px; /* 增加标题和第一个输入框之间的间隔 */
}

/* 可选：移除最后一个元素的底部外边距 */
.inputx:last-child, .vs-button:last-child {
  margin-bottom: 20px;
}
</style>
