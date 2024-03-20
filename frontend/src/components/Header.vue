<template>
  <div class="header">
    <h1>探索之旅</h1>
    <div class="buttons">
      <button class="register-button" @click="registerUser">注册</button>
      <button class="help-button" @click="openHelpCenter">帮助中心</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';

const registerUser = async () => {
  try {
    const response = await axios.post('/api/users/register', {
      username: 'user1',
      email: 'user1@example.com',
      password: 'password123'
    });
    console.log(response.data);
    alert('用户注册成功！');
  } catch (error) {
    if (error.response.status === 400) {
      console.error(error.response.data.error);
      alert('注册失败：' + error.response.data.error);
    } else {
      console.error('注册请求出错：', error.message);
      alert('注册请求出错：' + error.message);
    }
  }
};

const openHelpCenter = () => {
  // 打开帮助中心功能逻辑
  console.log('点击了帮助中心按钮');
};
</script>

<style scoped>
.header {
  background-color: #add8e6; /* 浅蓝色背景 */
  width: 1410px; /* 宽度400像素 */
  padding: 20px; /* 上下左右内边距20像素 */
  display: flex;
  justify-content: space-between; /* 按钮之间的空间均匀分布 */
}

.header h1 {
  margin: 0; /* 去除标题的默认外边距 */
  margin-left: 50px; /* 距离左边50像素 */
  font-family: "Comic Sans MS", cursive, sans-serif; /* 生动活泼的字体 */
}

.buttons {
  display: flex;
}

.register-button,
.help-button {
  padding: 8px 20px; /* 调整按钮大小 */
  margin-right: 50px; /* 注册按钮距离帮助中心按钮的右边界50像素 */
}

.register-button {
  background-color: #007bff; /* 蓝色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.help-button {
  background-color: #28a745; /* 绿色 */
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.register-button:hover,
.help-button:hover {
  background-color: #0056b3; /* 鼠标悬停时的背景色 */
}
</style>
