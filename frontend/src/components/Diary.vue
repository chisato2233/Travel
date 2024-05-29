<template>
  <div class="diary">
    <h2>我的日记</h2>
    
    <!-- 添加日记按钮 -->
    <router-link :to="{ name: 'CreateDiary' }" class="btn-add">+</router-link>

    <!-- 展示用户日记列表 -->
    <div v-if="diaries.length > 0">
      <ul class="diary-list">
        <li v-for="diary in sortedDiaries" :key="diary.id" class="diary-item">
          <h3>{{ diary.title }}</h3>
          <p>{{ diary.content }}</p>
          <p>日期: {{ diary.date }}</p>
          <p>地点: {{ diary.location }}</p>
          <!-- 更新日记按钮 -->
          <button @click="updateDiary(diary)" class="btn-update">更新日记</button>
          <!-- 删除日记按钮 -->
          <button @click="deleteDiary(diary.id)" class="btn-delete">删除日记</button>
        </li>
      </ul>
    </div>
    <p v-else class="no-diaries">暂无日记。</p>
    
    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue';

const diaries = ref([]); // 存储用户日记列表
const router = useRouter();

// 获取用户日记列表的方法
const fetchDiaries = async () => {
  const token = localStorage.getItem('token'); // 从 localStorage 获取 token
  if (!token) {
    console.error('Token not found');
    return;
  }
  console.log('Using token:', token);
  try {
    const response = await axios.get('http://localhost:8000/api/diaries/my-diaries/', {
      headers: {
        'Authorization': `Bearer ${token}` // 在请求头中添加 Authorization
      }
    });
    diaries.value = response.data; // 将获取到的日记列表存储到 diaries 变量中
  } catch (error) {
    if (error.response && error.response.status === 401) {
      // 跳转到登录页面
      console.error('未经授权的访问。');
      router.push('Login/');
    } else {
      console.error('获取用户日记失败：', error);
    }
  };
}

// 在组件加载时调用 fetchDiaries 函数，获取用户日记列表
onMounted(fetchDiaries);

// 计算属性：按日期排序的日记列表
const sortedDiaries = computed(() => {
  return diaries.value.slice().sort((a, b) => new Date(b.date) - new Date(a.date));
});

// 更新日记
const updateDiary = (diary) => {
  // 导航到更新界面，并将当前选中的日记内容传递给 UpdateDiary.vue
  router.push({ name: 'UpdateDiary', params: { diaryData: diary } });
}

// 删除日记
const deleteDiary = async (diaryId) => {
  const token = localStorage.getItem('token');
  if (!token) {
    console.error('Token not found');
    return;
  }
  try {
    const response = await axios.delete(`http://localhost:8000/api/diaries/delete/${diaryId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    console.log(response.data.message); // 输出删除成功的消息
    // 删除成功后，重新获取日记列表以更新界面
    await fetchDiaries();
  } catch (error) {
    if (error.response && error.response.status === 404) {
      console.error('日记未找到。');
    } else {
      console.error('删除日记失败：', error);
    }
  }
}
</script>

<style scoped>
.diary {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.diary-list {
  list-style: none;
  padding: 0;
}

.diary-item {
  margin-bottom: 20px;
}

.no-diaries {
  color: #888;
}

.btn-add {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #28a745;
  color: #fff;
  font-size: 24px;
  border: none;
  cursor: pointer;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-update {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  background-color: #007bff; /* 蓝色背景 */
  color: #fff; /* 白色字体 */
  cursor: pointer;
  font-size: 14px;
  margin-top: 5px;
}

.btn-delete {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  background-color: #dc3545; /* 红色背景 */
  color: #fff; /* 白色字体 */
  cursor: pointer;
  font-size: 14px;
  margin-top: 5px;
}
</style>
