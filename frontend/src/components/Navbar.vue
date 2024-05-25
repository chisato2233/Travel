<!-- 这是导航栏，有4个选项 1. 首页（HomePage.vue），2. 寻路（Travel.vue），
                         3. 日记(Diary.vue)，     4. 我的(UserInfo.vue) -->

<!-- 若未登录点击日记会直接跳转到登录界面（Login.vue） -->
<!-- 若未登录点击我的会直接跳转到登录界面（Login.vue） -->

<template>
  <div class="navbar">
    <router-link to="/" class="nav-item">首页</router-link>
    <router-link to="/travel" class="nav-item">寻路</router-link>
    <router-link :to="diaryLink" class="nav-item">日记</router-link>
    <router-link :to="profileLink" class="nav-item">我的</router-link>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex'; // 引入 Vuex 中的 store

const store = useStore(); // 获取 Vuex store 实例
async function isLoggedIn() {
  // try {
  //   const response = await axios.get('http://localhost:8000/api/users/check-auth', {
  //     headers: {
  //       Authorization: `Bearer ${localStorage.getItem('token')}`
  //     }
  //   });

  //   return response.data.isLoggedIn;
  // } catch (error) {
  //   console.error('检查用户登录状态失败:', error);
  //   return false;
  // }
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
// 计算属性，根据用户登录状态决定跳转路径
const diaryLink = computed(() => {
  return localStorage.getItem("token") ? '/diary' : '/login';
});

// 计算属性，根据用户登录状态决定跳转路径
const profileLink = computed(() => {
  return localStorage.getItem("token") ? '/profile' : '/login';
});
</script>

<style scoped>
.navbar {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #008000; /* 绿色背景 */
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
  border-top: 1px solid #ccc;
}

.nav-item {
  text-decoration: none;
  color: #fff; /* 白色字体 */
  cursor: pointer;
  font-weight: bold; /* 加粗字体 */
}
</style>


