<template>
  <div class="diary">
    <h2>创建日记</h2>
    <!-- 创建日记表单 -->
    <form @submit.prevent="createDiary" class="diary-form">
      <input type="text" v-model="newDiary.title" placeholder="标题" class="input-field">
      <textarea v-model="newDiary.content" placeholder="内容" class="textarea-field"></textarea>
      <input type="date" v-model="newDiary.date" placeholder="日期" class="input-field">
      <input type="text" v-model="newDiary.location" placeholder="地点" class="input-field">
      <button type="submit" class="btn-create">创建日记</button>
    </form>

    <h2>我的日记</h2>
    <!-- 展示用户日记列表 -->
    <div v-if="diaries.length > 0">
      <ul class="diary-list">
        <li v-for="diary in diaries" :key="diary.id" class="diary-item">
          <h3>{{ diary.title }}</h3>
          <p>{{ diary.content }}</p>
          <p>日期: {{ diary.date }}</p>
          <p>地点: {{ diary.location }}</p>
          <!-- 更新日记按钮 -->
          <button @click="updateDiary(diary.id)" class="btn-update">更新日记</button>
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
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from './Navbar.vue';

const diaries = ref([]); // 存储用户日记列表
const newDiary = ref({
  title: '',
  content: '',
  date: '',
  location: ''
}); // 用于存储新日记的数据

// 在页面加载时获取用户日记列表
onMounted(async () => {
  await fetchDiaries();
});

//创建日记
const createDiary = async () => {
  try {
    // 从 localStorage 中获取用户 token
    const token = localStorage.getItem('token');

    if (!token) {
      console.error('用户未登录或登录状态已过期');
      return;
    }

    // 获取当前登录用户的信息
    const userResponse = await axios.get('http://localhost:8000/api/users/user', {
      headers: {
        Authorization: `Bearer ${token}` // 使用存储在 localStorage 中的用户 token
      }
    });

    // 从用户信息中获取用户ID
    const userId = userResponse.data.id;

    // 发送创建日记的请求，包括用户ID
    const response = await axios.post('http://localhost:8000/api/diaries/create/', {
      title: newDiary.value.title,
      content: newDiary.value.content,
      date: newDiary.value.date,
      location: newDiary.value.location,
      userId: userId // 使用当前登录用户的ID
    });

    if (response.status === 201) {
      console.log(response.data.message); // 打印成功消息
      await fetchDiaries(); // 刷新日记列表
      // 清空新日记数据
      newDiary.value = {
        title: '',
        content: '',
        date: '',
        location: ''
      };
    }
  } catch (error) {
    if (error.response) {
      if (error.response.status === 400) {
        console.error('缺少或无效的日记信息。');
      } else if (error.response.status === 401) {
        console.error('未经授权的访问。');
      } else if (error.response.status === 404) {
        console.error('未找到日记。');
      }
    } else {
      console.error('创建日记失败：', error);
    }
  }
};


const updateDiary = async (diaryId, updatedDiary) => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('用户未登录或登录状态已过期');
      return;
    }

    // 发送更新日记的请求，包括用户 token 和更新后的日记内容
    const response = await axios.put(`http://localhost:8000/api/diaries/update/${diaryId}/`, updatedDiary, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (response.status === 200) {
      console.log(response.data.message); // 打印成功更新日记的消息
      await fetchDiaries(); // 更新日记后刷新日记列表
    }
  } catch (error) {
    console.error('更新日记失败：', error);
  }
};


// 删除日记的方法
const deleteDiary = async (diaryId) => {
  try {
    const response = await axios.delete(`http://localhost:8000/api/diaries/delete/${diaryId}/`);
    console.log(response.data.message); // 打印成功删除日记的消息
    await fetchDiaries(); // 删除日记后刷新日记列表
  } catch (error) {
    console.error('删除日记失败：', error);
  }
};

// 获取用户日记列表的方法
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
      // 访问令牌无效或过期，提示用户重新登录
      console.error('访问令牌无效或过期，请重新登录。');
      localStorage.removeItem('token'); // 清除存储的令牌
      // 重定向到登录页面或者显示登录对话框
      router.push('Login/')
    } else {
      console.error('获取用户日记失败：', error);
    }
  };
}


</script>

<style scoped>
.diary {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.diary-form {
  margin-bottom: 20px;
}

.input-field,
.textarea-field {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-create,
.btn-update,
.btn-delete {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  margin-right: 10px;
  background-color: #28a745; /* 绿色背景 */
  color: #fff; /* 白色字体 */
  cursor: pointer;
  font-weight: bold; /* 加粗字体 */
}

.btn-create:hover,
.btn-update:hover,
.btn-delete:hover {
  background-color: #218838; /* 深绿色背景 */
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
</style>
