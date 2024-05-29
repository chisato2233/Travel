<template>
  <div class="update-diary">
    <h2>更新日记</h2>
    
    <!-- 更新日记表单 -->
    <form @submit.prevent="updateDiary" class="diary-form">
      <input type="text" v-model="updatedDiary.title" placeholder="标题" class="input-field">
      <textarea v-model="updatedDiary.content" placeholder="内容" class="textarea-field"></textarea>
      <input type="date" v-model="updatedDiary.date" placeholder="日期" class="input-field">
      <input type="text" v-model="updatedDiary.location" placeholder="地点" class="input-field">
      <button type="submit" class="btn-update">更新日记</button>
    </form>

    <!-- 提示用户更新失败 -->
    <p v-if="updateError" class="error-message">{{ updateError }}</p>
    
    <!-- 导航栏组件 -->
    <Navbar />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Navbar from './Navbar.vue';

const router = useRouter();
const diaryData = JSON.parse(router.currentRoute.value.params.diaryData?.toString() || '{}');
const id = router.currentRoute.value.params.id; // 接收id参数


const updatedDiary = ref({
  id: diaryData.id,
  title: diaryData.title,
  content: diaryData.content,
  date: diaryData.date,
  location: diaryData.location
});
const updateError = ref('');

const updateDiary = async () => {
  try {
    const token = localStorage.getItem('token');
  
    if (!token) {
      console.error('用户未登录或登录状态已过期');
      router.push('Login/');
      return;
    }
  
    const response = await axios.put(`http://localhost:8000/api/diaries/update/${updatedDiary.value.id}`, {
      title: updatedDiary.value.title,
      content: updatedDiary.value.content,
      date: updatedDiary.value.date,
      location: updatedDiary.value.location
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
  
    if (response.status === 200) {
      console.log(response.data.message);
      // 更新成功后，返回日记列表页面
      router.push('/diary');
    }
  } catch (error) {
    if (error.response) {
      if (error.response.status === 400) {
        console.error('缺少或无效的更新信息。');
        updateError.value = '缺少或无效的更新信息，请重新填写。';
      } else if (error.response.status === 401) {
        console.error('未经授权的访问。');
        router.push('Login/');
      } else if (error.response.status === 404) {
        console.error('未找到日记。');
        updateError.value = '未找到日记，请稍后重试。';
      }
    } else {
      console.error('更新日记失败：', error);
      updateError.value = '更新日记失败，请稍后重试。';
    }
  }
};
</script>

<style scoped>
.update-diary {
  max-width: 600px;
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

.btn-update {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #46ca35; /* 蓝色背景 */
  color: #fff; /* 白色字体 */
  cursor: pointer;
  font-weight: bold; /* 加粗字体 */
}

.btn-update:hover {
  background-color: #066a04; /* 深蓝色背景 */
}

.error-message {
  color: #ff0000;
}
</style>
